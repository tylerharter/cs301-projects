import os
import glob
import json
import shutil
import subprocess
import sys
from collections import OrderedDict

import structlog
from colorama import Fore, Style

import tacli.utils
import tacli.helpers

log = structlog.get_logger()

@tacli.utils.pass_obj_as_args
def jump_cmd(state, review_num):
    tacli.helpers.modify_head(state, abs_val=review_num)

@tacli.utils.pass_obj_as_args
def prev_cmd(state):
    tacli.helpers.modify_head(state, inc_or_dec=-1)

@tacli.utils.pass_obj_as_args
def next_cmd(state):
    tacli.helpers.modify_head(state, inc_or_dec=1)

@tacli.utils.pass_obj_as_args
def difftool_cmd(state):
    meta = state['files'][state['head']]
    filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.review_dir)
    ref_filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.submissions_dir)
    tacli.utils.launch_difftool(ref_filepath, filepath)
    tacli.helpers.normalize(filepath)

@tacli.utils.pass_obj_as_args
def diff_cmd(state):
    meta = state['files'][state['head']]
    filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.review_dir)
    ref_filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.submissions_dir)
    os.system("diff {} {}".format(ref_filepath, filepath))

@tacli.utils.pass_obj_as_args
def check_token_cmd():
    user, token = tacli.helpers.get_user_token()
    log.info("Success!", user=user)

@tacli.utils.pass_obj_as_args
def exec_cmd(state):
    """
    executes the current file (This trusts the code - UNSAFE!)
    """

    meta = state['files'][state['head']]
    filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.review_dir)
    filename = os.path.basename(filepath)

    if filename!= "main.py":
        log.warn("Filename is not main.py! Remember to issue a warning", filename=filename)

    # NOTE this trusts the user program !!!
    shutil.copy(filepath, os.path.join(tacli.constants.repo_dir, "main.py"))
    with tacli.utils.chdir(tacli.constants.repo_dir):
        subprocess.call([sys.executable, "test.py"])

@tacli.utils.pass_obj_as_args
def list_cmd(state):
    """
    displays all the files to be reviewed along with status info
    """

    head = state['head']
    lines = []
    for idx, meta in enumerate(state['files']):
        line = []
        head_color = Fore.WHITE
        if idx == head:
            head_color = Fore.GREEN

        line.append(head_color)
        line.append("[{:<2}] ".format(idx))
        line.append("[{:<15}] ".format(meta['net_id']))
        line.append(Style.RESET_ALL)

        # duplicating lines for color alignment
        if meta['reviewed']:
            line.append(Fore.YELLOW + "(reviewed) " + Style.RESET_ALL)
        elif meta['_reviewed']:
            line.append(Fore.WHITE  + "(reviewed) " + Style.RESET_ALL)
        else:
            line.append(Fore.WHITE  + "           " + Style.RESET_ALL)

        if meta['modified']:
            line.append(Fore.RED + Style.BRIGHT + "(modified) " + Style.RESET_ALL)
        else:
            line.append(Fore.RED + Style.BRIGHT + "           " + Style.RESET_ALL)

        if not meta['has_main']:
            line.append(Fore.RED + Style.BRIGHT + "(no main.py) " + Style.RESET_ALL)
        else:
            line.append(Fore.RED + Style.BRIGHT + "             " + Style.RESET_ALL)

        line = ''.join(line)
        lines.append(line)

    for line1, line2 in zip(lines[:len(lines)//2], lines[len(lines)//2:]):
        print("{} {}".format(line1, line2))

    if len(lines) % 2 == 1:
        print(lines[-1])

@tacli.utils.pass_obj_as_args
def pull_cmd(project_id, skip_already_reviewed=False):
    """
    Pulls the content for the given project id
    """
    if os.path.exists("p{}".format(project_id)):
        log.error("p{} already exists!".format(project_id))
        return

    os.makedirs("p{}".format(project_id))
    os.chdir("p{}".format(project_id))

    user, token = tacli.helpers.get_user_token()

    if os.path.exists(tacli.constants.state_file):
        log.error("Current dir already has a state file, move to a fresh new dir")
        return

    log.info("getting project from github", project=project_id, dst=tacli.constants.repo_dir)
    tacli.helpers.get_project_from_github(project_id, tacli.constants.repo_dir)

    log.info("getting submissions", project=project_id, dst=tacli.constants.submissions_dir)
    os.makedirs(tacli.constants.submissions_dir)

    with tacli.utils.chdir(tacli.constants.submissions_dir):
        files = tacli.helpers.get_submissions(project_id, user, token, skip_already_reviewed)

    log.info("copying submissions", dst=tacli.constants.review_dir)
    shutil.copytree(tacli.constants.submissions_dir, tacli.constants.review_dir,
        copy_function=tacli.helpers.copy_and_make_src_readonly,
    )

    state = OrderedDict()
    state['num_files'] = len(files)
    state['head'] = 0
    state['files'] = files
    tacli.utils.dump_state(state)

@tacli.utils.pass_obj_as_args
def push_cmd(state, push_all=False):
    """
    Gathers all reviews and uploads them in a format
    compatible with the online tool
    """
    if push_all:
        # TODO push all
        return

    review_num = state['head']
    user, token = tacli.helpers.get_user_token()

    meta = state['files'][review_num]
    filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.review_dir)
    ref_filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.submissions_dir)
    try:
        global_review, line_reviews, deductions = tacli.helpers.get_reviews(ref_filepath, filepath)
        reviewed = len(global_review) > 0 or len(line_reviews) > 0
    except ValueError:
        log.error("Code modified, not pushing")
        return

    filemeta = tacli.helpers.get_meta_from_netid(meta['net_id'], base=tacli.constants.submissions_dir)

    highlights = {filemeta['filename']: line_reviews}
    tacli.helpers.put_code_review(
        token,
        filemeta['project_id'],
        filemeta['submitter_id'],
        filemeta['submission_id'],
        global_review,
        highlights,
        deductions,
    )



@tacli.utils.pass_obj_as_args
def edit_cmd(state):
    """
    Opens up an editor for the current file
    """

    meta = state['files'][state['head']]
    filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.review_dir)
    ref_filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.submissions_dir)

    tacli.utils.launch_editor(filepath)

    code_modified = False
    reviewed = False
    try:
        global_review, line_reviews, deductions = tacli.helpers.get_reviews(ref_filepath, filepath)
        reviewed = len(global_review) > 0 or len(line_reviews) > 0
        log.info("has global review?", ans=len(global_review) > 0)
        log.info("num line reviews", num=len(line_reviews))
        log.info("num deductions", num=deductions)
    except ValueError:
        code_modified = True

    if code_modified or reviewed:
        state['files'][state['head']]['modified'] = code_modified
        state['files'][state['head']]['reviewed'] = reviewed
        tacli.utils.dump_state(state)

@tacli.utils.pass_obj_as_args
def refresh_cmd(state):
    """
    recalculates modifications/reviews
    """

    for meta in state['files']:
        filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.review_dir)
        ref_filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.submissions_dir)

        code_modified = False
        reviewed = False
        try:
            global_review, line_reviews, deductions = tacli.helpers.get_reviews(ref_filepath, filepath)
            reviewed = len(global_review) > 0 or len(line_reviews) > 0
        except ValueError:
            code_modified = True

        meta['modified'] = code_modified
        meta['reviewed'] = reviewed

    tacli.utils.dump_state(state)
    list_cmd(state)

@tacli.utils.pass_obj_as_args
def expand_cmd(state, overwrite=False):
    """
    expands all macros in the modified file (useful for debugging?)
    """

    macros = tacli.helpers.get_macros()
    if len(macros) == 0:
        log.error("No macros detected")
        return

    meta = state['files'][state['head']]
    filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.review_dir)
    with open(filepath) as fp:
        lines = fp.readlines()

    fp = sys.stdout
    overwrite_path = filepath + ".tmp"
    if overwrite:
        fp = open(overwrite_path, 'w')

    for line in lines:
        if line.strip().startswith('#%'):
            key = line.strip()[2:].strip()
            if key in macros:
                macrolines = []
                line = line.expandtabs()
                leading_spaces = ' ' * (len(line) - len(line.lstrip()))
                macrolines = ['{}#% {}'.format(leading_spaces, l) for l in macros[key]]
                line = '\n'.join(macrolines) + '\n'

        fp.write(line)

    if overwrite:
        fp.close()
        shutil.move(overwrite_path, filepath)

@tacli.utils.pass_obj_as_args
def dump_cmd(state):
    """
    dumps the reviews for the current file
    """
    meta = state['files'][state['head']]
    filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.review_dir)
    ref_filepath = tacli.helpers.get_py_from_netid(meta['net_id'], base=tacli.constants.submissions_dir)

    global_review, line_reviews, deduction = '', [], 0
    try:
        global_review, line_reviews, deductions = tacli.helpers.get_reviews(ref_filepath, filepath)
    except ValueError:
        log.error("code modified, cannot dump highlights")

    print(Fore.YELLOW + global_review + Style.RESET_ALL)

    line_reviews = sorted(line_reviews, key=lambda x: x['offset'])
    with open(ref_filepath) as fp:
        for num, highlight in enumerate(line_reviews, 1):
            fp.seek(highlight['offset'])
            data = fp.read(highlight['length'])
            print(Fore.GREEN + "[{}]".format(num) + Style.RESET_ALL)
            print(Fore.GREEN + data + Style.RESET_ALL)
            print(Fore.YELLOW + highlight['comment'] + Style.RESET_ALL)

