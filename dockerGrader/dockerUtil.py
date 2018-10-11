import base64, boto3, botocore, logging, os, sys, json, subprocess, shutil, time, traceback

logging.basicConfig(
    handlers=[
        logging.FileHandler("dockerUtil.log"),
        logging.StreamHandler()
    ],
    level=logging.INFO)

ACCESS_PATH = "projects/{project}/users/{googleId}/curr.json"
CODE_DIR = "./submission"
TEST_DIR = "/tmp/test/{netId}"
SUBMISSIONS = 'submissions'
BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

def getCurrentUID():
    userName = os.environ.get("USER")
    if not userName:
        logging.warning("Invalid userName.")
    r = int(subprocess.check_output(["id", "-u", userName]))
    logging.info("Current user: {}, current uid: {}".format(userName, r))
    return r

currentUID = getCurrentUID()

def downloadSubmission(projectPath, testDir):
    # a project path will look something like this:
    # projects/p0/users/115799594197844895033/curr.json

    userId = projectPath.split('/')[-2]
    logging.info('download to {}'.format(testDir))

    # download
    response = s3.get_object(Bucket=BUCKET, Key=projectPath)
    submission = json.loads(response['Body'].read().decode('utf-8'))
    fileContents = base64.b64decode(submission.pop('payload'))
    fileName = submission['filename']
    # override the filename if it is a python source file
    if len(fileName) >= 3 and fileName[-2:] == 'py':
        fileName = "main.py"
    with open(os.path.join(testDir, fileName), 'wb') as f:
        f.write(fileContents)

def uploadResult(project, netId, errorLog = None):
    curTestDir = TEST_DIR.format(netId=netId)
    if errorLog:
        serializedResult = json.dumps(errorLog)
    else:
        try:
            with open("{}/result.json".format(curTestDir), "r") as fr:
                serializedResult = fr.read()
        except:
            serializedResult = json.dumps({"score":0, "error": "result not found"})
    s3.put_object(
        Bucket=BUCKET,
        Key='ta/grading/{}/{}.json'.format(project, netId),
        Body=serializedResult.encode('utf-8'),
        ContentType='text/plain')
    shutil.rmtree(curTestDir)

def lookupGoogleId(netId):
    path = 'users/net_id_to_google/%s.txt' % netId
    try:
        response = s3.get_object(Bucket=BUCKET, Key=path)
        net_id = response['Body'].read().decode('utf-8')
        return net_id
    except botocore.exceptions.ClientError as e:
        if not e.response['Error']['Code'] == "NoSuchKey":
            # unexpected error
            logging.warning(
                'Unexpected error when look up Googlg ID:' + e.response['Error']['Code'])
            raise e

def fetchFromS3(project, netId, testDir):
    googleId = lookupGoogleId(netId)
    if not googleId:
        return None
    curPath = ACCESS_PATH.format(project=project, googleId=googleId)
    downloadSubmission(curPath, testDir)

def containerStatus(containerId):
    checkCmd = ["docker", "inspect", "-f", "{{.State.ExitCode}} {{.State.Running}}", containerId]
    try:
        output = subprocess.check_output(checkCmd).decode("ascii").replace("\n","")
    except:
        logging.info("conatiner {} not existed.".format(containerId))
        return None, None
    response = output.split(' ')
    str2bool = {"false" : False, "true" : True}
    if len(response) == 2:
        return int(response[0]), str2bool[response[1]]
    else:
        logging.warning("Unexpected response when checking the container {} running status. Response: {}".format(containerId, output))
        return None, None

def rmContainer(containerId):
    forceRmCmd = ["docker", "rm", "-f", containerId]
    try:
        subprocess.check_output(forceKillCmd)
    except:
        logging.info("rm cantainer failed. ID: {}".format(containerId))

def dockerLiveCheck(project, netId, containerId, hardLimit = False):
    exitCode, isRunning = containerStatus(containerId)
    if isRunning:
        if hardLimit:
            uploadResult(project, netId, {"score":0, "error":"Timeout"})
            logging.info("project: {}, netid: {}, timeout".format(project, netId))
        else:
            logging.info("project: {}, netid: {}, soft limit check failed.".format(project, netId))
            return True
    elif exitCode:
        uploadResult(project, netId, {"score":0, "error":"ExitCode:" + str(exitCode)})
        logging.info("project: {}, netid: {}, exit with {}".format(project, netId, exitCode))
    else:
        uploadResult(project, netId)
        logging.info("project: {}, netid: {}, docker exit normally".format(project, netId))
    return False

def dockerRun(project, netId):
    # create directory to mount inside a docker container
    curTestDir = TEST_DIR.format(netId=netId)
    if os.path.exists(curTestDir):
        shutil.rmtree(curTestDir)
    os.makedirs(curTestDir)
    fetchFromS3(project, netId, curTestDir)

    # we can't use shutil.copytree here again because TEST_DIR exists
    testCodePath = "./test/{}".format(project)
    for item in os.listdir(testCodePath):
        src = os.path.join(testCodePath, item)
        dest = os.path.join(curTestDir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)

    # run tests inside a docker container
    image = 'python:3.7-stretch' # TODO: find/build some anaconda image
    cmd = ['docker', 'run',                           # start a container
           '-d',                                      # detach mode
           '--rm',                                    # remove the container when exit
           '-v', os.path.abspath(curTestDir)+':/code',  # share the test dir inside
           '-u', str(currentUID),                     # run as local user (instead of root)
           '-w', '/code',                             # working dir is w/ code
           image,                                     # what docker image?
           'python3', 'test.py',
           '-p', project,
           '-i', netId]                      # command to run inside
    logging.info("docker cmd:" + ' '.join(cmd))
    containerId = subprocess.check_output(cmd).decode("ascii").replace("\n","")
    logging.info("container id:" + containerId)
    time.sleep(1)
    if dockerLiveCheck(project, netId, containerId):
        time.sleep(3)
        dockerLiveCheck(project, netId, containerId, hardLimit = True)
    rmContainer(containerId)
