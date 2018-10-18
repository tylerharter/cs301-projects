import base64
import os
import glob
import json
import subprocess
import shutil
import stat
import sys
import time
from hashlib import md5

import boto3
import requests
import structlog

import tacli.utils
import tacli.constants

log = structlog.get_logger()

def get_user_from_token(token):
    url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}'.format(token=token)
    resp = requests.get(url)
    if resp.status_code != 200:
        log.error("Bad Token, could not lookup email")
        log.info("Sign In at the following url and copy new token", url=tacli.constants.signin_url)
        sys.exit()

    data = resp.json()
    return data['email']

def get_user_token():
    """
    gets user email and token
    """

    token = os.environ.get(tacli.constants.tacli_token_env, None)
    if token is not None:
        return get_user_from_token(token), token

    log.info("save your token in the environmental variable {} to skip this step in future!".format(tacli.constants.tacli_token_env))
    log.info("Sign In at the following url, copy the token and paste it into the editor", url=tacli.constants.signin_url)
    time.sleep(2)
    tacli.utils.launch_editor("token")
    with open("token") as fp:
        token = fp.read().strip()

    return get_user_from_token(token), token

def copy_and_make_src_readonly(src, dst, *args, **kwargs):
    shutil.copy2(src, dst, *args, **kwargs)
    if os.path.exists(dst):
        # make src read only once copy is successful
        os.chmod(src, stat.S_IRUSR)

def get_project_from_github(project_id, dst):
    """
    downloads the project from github into dst folder
    """

    cmds = [
        "git init",
        "git config core.sparseCheckout true",
        "git remote add -f origin {}".format(tacli.constants.repo_link),
        'echo "fall18/p{}/*" > .git/info/sparse-checkout'.format(project_id),
        "git checkout master",
    ]
    cmd = ' && '.join(cmds)
    dst = os.path.abspath(dst)

    os.makedirs(".tmp_git_repo")
    with tacli.utils.chdir(".tmp_git_repo"):
        subprocess.check_call(cmd, shell=True)
        shutil.move("fall18/p{}".format(project_id), dst)

    shutil.rmtree(".tmp_git_repo")

    with tacli.utils.chdir(dst):
        # for reference if we need to look at it
        if os.path.exists("main.py"):
            shutil.move("main.py", "original_main.py")

def _lazy_client(cache={}):
    if 'client' in cache:
        return cache['client']

    session = boto3.Session(profile_name=tacli.constants.aws_cred_profile)
    s3 = session.client('s3')
    cache['client'] = s3
    return s3

def download_submission(net_id, path, submitter_id):
    s3 = _lazy_client()
    response = s3.get_object(Bucket=tacli.constants.s3_bucket, Key=path)
    submission = json.loads(response['Body'].read().decode('utf-8'))
    file_contents = base64.b64decode(submission.pop('payload'))

    os.makedirs(net_id)
    with open(os.path.join(net_id, submission['filename']), 'wb') as f:
        f.write(file_contents)

    # TODO handle zip files
    normalize(os.path.join(net_id, submission['filename']))
    submission['submitter_id'] = submitter_id
    with open(os.path.join(net_id, 'meta.json'), 'w') as f:
        f.write(json.dumps(submission, indent=2))

    return submission

def normalize(f):
    with open(f, 'rU') as fp:
        data = fp.read()

    data = data.rstrip()
    with open(f, 'w') as fp:
        fp.write(data)

def get_submissions(project_id, user, token, skip_already_reviewed):
    """
    downloads all submissions for current user into scratch space
    """
    project_id = "p{}".format(project_id)

    payload = {
        "fn": tacli.constants.fn_list_submissions,
        "project_id": project_id,
        "GoogleToken": token,
    }

    response = requests.post(tacli.constants.cs301_lambda_endpoint, json=payload)
    data = response.json()
    if not 200 <= data['statusCode'] < 300:
        log.error("bad status code, invalid google token?", status_code=data['statusCode'])
        sys.exit()

    files = []

    submissions = data['body']['submissions']
    for entry in submissions:
        assert entry['project_id'] == project_id, "{} not same as {}!".format(entry['project_id'], project_id)
        info = entry['info']
        net_id = info['net_id']

        ta = info.get('ta')

        if ta != user:
            continue

        if entry['has_review'] and skip_already_reviewed:
            continue

        submission = download_submission(net_id, entry['path'], entry['submitter_id'])
        has_main = False
        if submission['filename'] == "main.py":
            has_main = True

        meta = {
            "net_id": net_id,
            "_reviewed": entry['has_review'],
            "reviewed": False,
            "modified": False,
            "has_main": has_main,
        }

        files.append(meta)

    files = sorted(files, key=lambda x: x['net_id'])
    return files

def get_py_from_netid(net_id, base):
    meta_file = os.path.join(base, net_id, "meta.json")
    with open(meta_file) as fp:
        filename = json.load(fp)['filename']

    return os.path.join(base, net_id, filename)

def get_meta_from_netid(net_id, base):
    meta_file = os.path.join(base, net_id, "meta.json")
    with open(meta_file) as fp:
        return json.load(fp)

def modify_head(state, abs_val=None, inc_or_dec=None):
    """
    changes the head in the state file
    """

    if abs_val is not None:
        if abs_val < 0 or abs_val >= state['num_files']:
            log.error("invalid jump!", value=abs_val)
            return

        state['head'] = abs_val

    elif inc_or_dec is not None:
        new_head = state['head'] + inc_or_dec
        if new_head < 0 or new_head >= state['num_files']:
            log.error("invalid jump!", value=new_head)
            return

        state['head'] = new_head
    else:
        return

    tacli.utils.dump_state(state)
    log.info("head updated!", at=state['head'], net_id=state['files'][state['head']]['net_id'])

def get_reviews(original, modified):
    modified_without_reviews_hash = md5()
    original_hash = md5()
    line_reviews = []
    global_review = []
    deductions = []

    # this removes the \n being appended in the end unnecessarily
    normalize(modified)

    with open(modified) as fp:
        line_num = 1
        line_num_to_reviews = {}
        for line in fp:
            if line.lstrip().startswith(tacli.constants.review_prefix):
                # if line num is 1, then this is global stuff like deductions and general
                # comments
                if line_num == 1:
                    global_review.append(line.strip()[2:])
                else:
                    line_num_to_reviews.setdefault(line_num, []).append(line.strip()[2:])
            else:
                modified_without_reviews_hash.update(line.encode('utf-8'))
                line_num += 1

    # expand all macros
    if os.path.exists(tacli.constants.macro_file):
        macros = tacli.helpers.get_macros()
        _line_num_to_reviews = {}
        for line_num, lines in line_num_to_reviews.items():
            new_lines = []
            _line_num_to_reviews[line_num] = new_lines
            for line in lines:
                macrolines = macros.get(line.strip())
                if macrolines is None:
                    new_lines.append(line)
                    continue

                new_lines.extend(macrolines)

        line_num_to_reviews = _line_num_to_reviews

        _global_review = []
        for line in global_review:
            macrolines = macros.get(line.strip())
            if macrolines is None:
                _global_review.append(line)
                continue
            _global_review.extend(macrolines)
        global_review = _global_review

    with open(original) as fp:
        fp.seek(0, 2) # seek to end
        last_pos = fp.tell()
        fp.seek(0)
        cur_pos = fp.tell()
        line_num = 1
        while cur_pos != last_pos:
            line_start_pos = cur_pos
            line = fp.readline()
            line_end_pos = fp.tell()
            original_hash.update(line.encode('utf-8'))
            if line_num in line_num_to_reviews:
                review = '\n'.join(line_num_to_reviews[line_num])
                line_reviews.append({'offset': line_start_pos, 'length': (line_end_pos - line_start_pos), 'comment': review})

            line_num += 1
            cur_pos = line_end_pos

    if original_hash.digest() != modified_without_reviews_hash.digest():
        raise ValueError("File contains more than just reviews")

    new_global_review = []
    deductions = []
    for line in global_review:
        if tacli.constants.deduct_keyword in line:
            m = tacli.constants.deduct_regex.match(line)
            if m is not None:
                deductions.append(int(m.group('score')))
                continue

        new_global_review.append(line)

    return '\n'.join(new_global_review), line_reviews, sum(deductions)

def get_macros():
    macros = {}

    if not os.path.exists(tacli.constants.macro_file):
        log.error("File not found!", loc=tacli.constants.macro_file)
        return macros

    headerlen = len(tacli.constants.macro_keyword)
    with open(tacli.constants.macro_file) as fp:
        current_macro_lines = []
        for line in fp:
            if line.startswith(tacli.constants.macro_keyword):
                # new macro found!
                current_macro_lines = []
                key = line[headerlen:].strip()
                macros[key] = current_macro_lines
                continue

            current_macro_lines.append(line.rstrip())

    # trim the first few and last few macro lines, but preserve empty ones in between
    _macros = {}
    for key, lines in macros.items():
        for start, line in enumerate(lines):
            if line.strip() != '':
                break

        for end, line in enumerate(lines[::-1]):
            if line.strip() != '':
                break

        end = len(lines) - end
        _macros[key] = lines[start:end]

    macros = _macros

    return macros

def put_code_review(token, project_id, submitter_id, submission_id, general_comments, highlights, deductions):
    if not project_id.startswith("p"):
        project_id = "p{}".format(project_id)

    if len(general_comments) == 0:
        log.error("Missing general comment!")
        return

    payload = {
        "GoogleToken": token,
        "fn": tacli.constants.fn_put_code_review,
        "project_id": project_id,
        "submitter_id": submitter_id,
        "cr": {
            "is_grader": True,
            "general_comments": general_comments,
            "points_deducted": deductions,
            "submission_id": submission_id,
            "highlights": highlights,
        },
    }

    response = requests.post(tacli.constants.cs301_lambda_endpoint, json=payload)
    data = response.json()
    if not 200 <= data['statusCode'] < 300:
        log.error("failed to post review", body=data['body'])
        return

    log.info("successfully posted review")
