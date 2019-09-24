import base64, boto3, botocore, os, sys, json, subprocess, shutil, time, traceback, logging, re, string
from datetime import datetime

BUCKET = 'caraza-harter-cs301'
SEMESTER = "fall19"
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')


def get_submissions(project, rerun, email=None):
    prefix = 'a/projects/' + project + '/'
    if email:
        if not '@' in email:
            email += '@wisc.edu'
        prefix += to_s3_key_str(email) + '/'

    submitted = set()
    tested = set()

    for path in s3_all_keys(prefix):
        parts = path.split('/')
        if parts[-1] == 'submission.json':
            submitted.add(path)
        elif parts[-1] == 'test.json':
            parts[-1] = 'submission.json'
            tested.add('/'.join(parts))
    if not rerun:
        submitted -= tested
    return submitted


def fetch_submission(s3path):
    local_dir = './s3/'+os.path.dirname(s3path)
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)
    os.makedirs(local_dir)

    response = s3.get_object(Bucket=BUCKET, Key=s3path)
    submission = json.loads(response['Body'].read().decode('utf-8'))
    fileContents = base64.b64decode(submission.pop('payload'))
    fileName = submission['filename']
    # override the filename if it is a python source file
    if len(fileName) >= 3 and fileName.endswith('.py'):
        fileName = "main.py"
    elif len(fileName) >= 6 and fileName.endswith('.ipynb'):
        fileName = "main.ipynb"
    with open(os.path.join(local_dir, fileName), 'wb') as f:
        f.write(fileContents)
    return local_dir


def run_test_in_docker(code_dir):
    # build with docker build . -t grader
    image = 'grader'

    cmd = ['docker', 'run',                           # start a container
           '-d',                                      # detach
           '-v', os.path.abspath(code_dir)+':/code',  # share the test dir inside
           '-w', '/code',                             # working dir is w/ code
           image,                                     # what docker image?
           'timeout', '60',                           # timeout
           'python3', 'test.py']                      # command to run inside

    print("RUN: " + " ".join(cmd))
    containerId = subprocess.check_output(cmd).decode("ascii").replace("\n","")
    t0 = time.time()
    print("CONTAINER", containerId)

    cmd = ["docker", "wait", containerId]
    print("RUN", " ".join(cmd))
    status = subprocess.check_output(cmd)
    t1 = time.time()

    # cleanup
    cmd = ["docker", "logs", containerId]
    print("RUN", " ".join(cmd))
    subprocess.check_output(cmd)
    logs = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    logs = logs.decode("ascii")
    # https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    logs = ansi_escape.sub('', logs)
    subprocess.check_output(["docker", "rm", containerId])

    # get result
    try:
        with open("{}/result.json".format(code_dir)) as f:
            result = json.load(f)
    except Exception as e:
        result = {
            "score":0,
            "error": str(e),
            "logs": logs.split("\n")
        }

    result["date"] = datetime.now().strftime("%m/%d/%Y")
    result["latency"] = t1 - t0
    print("Score:", result["score"])
    return json.dumps(result, indent=2)


def s3_all_keys(Prefix):
    ls = s3.list_objects_v2(Bucket=BUCKET, Prefix=Prefix, MaxKeys=10000)
    keys = []
    while True:
        print('...list_objects...')
        contents = [obj['Key'] for obj in ls.get('Contents',[])]
        keys.extend(contents)
        if not 'NextContinuationToken' in ls:
            break
        ls = s3.list_objects_v2(Bucket=BUCKET, Prefix=Prefix,
                                ContinuationToken=ls['NextContinuationToken'],
                                MaxKeys=10000)
    return keys


safe_s3_chars = set(string.ascii_letters + string.digits + ".-_")
def to_s3_key_str(s):
    s3key = []
    for c in s:
        if c in safe_s3_chars:
            s3key.append(c)
        elif c == "@":
            s3key.append('*at*')
        else:
            s3key.append('*%d*' % ord(c))
    return "".join(s3key)


def main():
    if len(sys.argv) < 3:
        print("Usage: python dockerUtil.py pX[pY,...] (<netId>|?) [-rerun]")
        sys.exit(1)

    print('\nTIP: run this if time is out of sync: sudo ntpdate -s time.nist.gov\n')

    if sys.argv[2] == '?':
        net_id = None
    else:
        net_id = sys.argv[2]

    rerun = True if '-rerun' in sys.argv else False

    safe = True if '-safe' in sys.argv else False

    projects = sys.argv[1].split(',')
    for project_id in projects:
        submissions = get_submissions(project_id, rerun=rerun, email=net_id)
        for s3path in sorted(submissions):
            print('========================================')
            print(s3path)

            codedir = fetch_submission(s3path)
            test = "../{}/{}/test.py".format(SEMESTER, project_id)
            shutil.copyfile(test, codedir+'/test.py')
            result = run_test_in_docker(codedir)
            
            if not safe:
                s3.put_object(
                    Bucket=BUCKET,
                    Key='/'.join(s3path.split('/')[:-1] + ['test.json']),
                    Body=result.encode('utf-8'),
                    ContentType='text/plain')


if __name__ == '__main__':
    main()
