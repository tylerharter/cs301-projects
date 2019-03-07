import base64, boto3, botocore, os, sys, json, subprocess, shutil, time, traceback, logging, re

SEMESTER = "spring19"
ACCESS_KEY = "projects/{project}/users/{googleId}/curr.json"
GOOGLE_KEY = "users/net_id_to_google/{netId}.txt"
UPLOAD_KEY = "ta/grading/{project}/{netId}.json"
ROSTER_KEY = "users/roster.json"
TEST_DIR = "/tmp/test/{netId}"
SUBMISSIONS = 'submissions'
BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

def fetchNetIds():
    response = s3.get_object(Bucket=BUCKET, Key=ROSTER_KEY)
    rows = json.loads(response['Body'].read().decode('utf-8'))
    return [row['net_id'] for row in rows]

class dockerGrader:
    def __init__(self, project, netId, logger):
        self.project = project
        self.netId = netId
        self.containerid = None
        self.logger = logger
        self.googleKey = GOOGLE_KEY.format(netId=self.netId)

        self.googleId = self.lookupGoogleId()
        self.currentUID = self.getCurrentUid()

        self.submissionKey = ACCESS_KEY.format(project=self.project, googleId=self.googleId)
        self.uploadKey = UPLOAD_KEY.format(project=self.project, netId=self.netId)

        self.testDir = TEST_DIR.format(netId=netId)

    # Util Functions
    def getCurrentUid(self):
        userName = os.environ.get("USER")
        if not userName:
            self.logger.warning("Invalid userName.")
        r = int(subprocess.check_output(["id", "-u", userName]))
        self.logger.info("current user: {}, current uid: {}".format(userName, r))
        return r

    def lookupGoogleId(self):
        try:
            response = s3.get_object(Bucket=BUCKET, Key=self.googleKey)
            netId = response['Body'].read().decode('utf-8')
            return netId
        except botocore.exceptions.ClientError as e:
            if not e.response['Error']['Code'] == "NoSuchKey":
                # unexpected error
                self.logger.warning(
                    'Unexpected error when look up Googlg ID:' + e.response['Error']['Code'])
                raise e

    def tryExtractResultScore(self, blob):
        try:
            result = json.loads(blob)
            if result and "upload" in result and not result["upload"]:
                return None
            return result.get('score', 0)
        except:
            return 0

    # Download Functions
    def downloadSubmission(self):
        if not self.googleId:
            return
        # a project path will look something like this:
        # projects/p0/users/115799594197844895033/curr.json
        self.logger.info('downloading {} to {}'.format(self.submissionKey, self.testDir))
        # download
        try:
            response = s3.get_object(Bucket=BUCKET, Key=self.submissionKey)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "NoSuchKey":
                self.logger.warning('no submission found')
                return False
            # unexpected error
            self.logger.warning(
                'Unexpected error when look up Googlg ID:' + e.response['Error']['Code'])
            raise e

        submission = json.loads(response['Body'].read().decode('utf-8'))
        fileContents = base64.b64decode(submission.pop('payload'))
        fileName = submission['filename']
        # override the filename if it is a python source file
        if len(fileName) >= 3 and fileName.endswith('.py'):
            fileName = "main.py"
        elif len(fileName) >= 6 and fileName.endswith('.ipynb'):
            fileName = "main.ipynb"
        with open(os.path.join(self.testDir, fileName), 'wb') as f:
            f.write(fileContents)
        return True

    def getRemoteResult(self):
        try:
            response = s3.get_object(Bucket=BUCKET, Key=self.uploadKey)
            return response['Body'].read().decode('utf-8')
        except:
            return json.dumps({"score":0, "error": "s3 fetching failed", "upload": False})

    def getLocalResult(self, errorLog = None):
        if errorLog:
            serializedResult = json.dumps(errorLog)
        else:
            try:
                with open("{}/result.json".format(self.testDir), "r") as fr:
                    serializedResult = fr.read()
            except:
                serializedResult = json.dumps({"score":0, "error": "result not found"})
        return serializedResult

    # Upload Functions
    def uploadResult(self, errorLog = None):
        serializedResult = self.getLocalResult(errorLog)
        s3.put_object(
            Bucket=BUCKET,
            Key=self.uploadKey,
            Body=serializedResult.encode('utf-8'),
            ContentType='text/plain')
        shutil.rmtree(self.testDir)

    # Container Operation Functions
    def containerStatus(self):
        checkCmd = ["docker", "inspect", "-f", "{{.State.ExitCode}} {{.State.Running}}", self.containerId]
        try:
            output = subprocess.check_output(checkCmd).decode("ascii").replace("\n","")
        except:
            self.logger.info("conatiner {} not existed.".format(self.containerId))
            return None, None
        response = output.split(' ')
        str2bool = {"false" : False, "true" : True}
        if len(response) == 2:
            return int(response[0]), str2bool[response[1]]
        else:
            self.logger.warning("Unexpected response when checking the container {} running status. Response: {}".format(self.containerId, output))
            return None, None

    def dockerLiveCheck(self, hardLimit = False):
        exitCode, isRunning = self.containerStatus()
        if isRunning:
            if hardLimit:
                self.uploadResult({"score":0, "error":"Timeout"})
                self.logger.info("project: {}, netId: {}, timeout".format(
                    self.project, self.netId))
            else:
                self.logger.info("project: {}, netId: {}, soft limit check failed.".format(
                    self.project, self.netId))
                return True
        elif exitCode:
            self.uploadResult({"score":0, "error":"ExitCode:" + str(exitCode)})
            self.logger.info("project: {}, netId: {}, exit with {}".format(
            self.project, self.netId, exitCode))
        else:
            self.uploadResult()
            self.logger.info("project: {}, netId: {}, docker exit normally".format(
                self.project, self.netId))
        return False

    def rmContainer(self):
        forceRmCmd = ["docker", "container", "rm", "-f", self.containerId]
        self.logger.info("rm container with the following command: {}".format(" ".join(forceRmCmd)))
        try:
            subprocess.check_output(forceRmCmd)
        except:
            self.logger.info("rm cantainer failed. ID: {}".format(self.containerId))

    def listTestScripts(self):
        testCodePath = "../{}/{}".format(SEMESTER, self.project)
        return [name for name in os.listdir(testCodePath) if re.match(r'test(\d+)?.py', name)]
            
    # Main Functions
    def dockerRun(self, test="test.py", upload=True):
        # create directory to mount inside a docker container
        if os.path.exists(self.testDir):
            shutil.rmtree(self.testDir)
        os.makedirs(self.testDir)

        # we can't use shutil.copytree here again because TEST_DIR exists
        testCodePath = "../{}/{}".format(SEMESTER, self.project)
        for item in os.listdir(testCodePath):
            src = os.path.join(testCodePath, item)
            dest = os.path.join(self.testDir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)

        # user's code
        res = self.downloadSubmission()
        if not res:
            return False

        # run tests inside a docker container
        image = 'grader' # build with docker build . -t grader
        cmd = ['timeout', '300',                           # set a timeout
               'docker', 'run',                           # start a container
               '--rm',                                    # remove the container when exit
               '-v', os.path.abspath(self.testDir)+':/code',  # share the test dir inside
               '-u', str(self.currentUID),                     # run as local user (instead of root)
               '-w', '/code',                             # working dir is w/ code
               image,                                     # what docker image?
               'timeout', '15',
               'python3', test]                      # command to run inside
        print("CMD: " + " ".join(cmd))
        try:
            subprocess.check_output(cmd).decode("ascii").replace("\n","")
        except Exception as e:
            self.logger.warning("docker run returns non-zero error code")

        if upload:
            self.uploadResult()

        return True

    # dockerRunSafe will check the existing grade first to avoid incorrect grade override
    def dockerRunSafe(self, test):
        try:
            resultOld = self.getRemoteResult()
            scoreOld = self.tryExtractResultScore(resultOld)
            if scoreOld == 100:
                self.logger.info('skip because old score was 100')
                return
            if not self.dockerRun(test=test, upload=False):
                self.logger.info('skip because submission not found')
                return
            resultNew = self.getLocalResult()
            scoreNew = self.tryExtractResultScore(resultNew)
            # only upload if new score is better
            self.logger.info("old score: {}, new score: {}".format(scoreOld, scoreNew))
            if scoreOld == None or scoreNew > scoreOld:
                self.logger.info('Uploading new score')
                self.uploadResult()
            self.logger.debug("new test results:")
            self.logger.debug(resultNew)
        except Exception as e:
            self.logger.error("Fatal error in dockerRun", exc_info=True)

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    if len(sys.argv) != 3:
        print("Usage: python dockerUtil.py pX[pY,...] (<netId>|?)")
        sys.exit(1)

    projects = sys.argv[1].split(',')
    if sys.argv[2] == '?':
        net_ids = fetchNetIds()
    else:
        net_ids = [sys.argv[2]]

    for project_id in projects:
        for net_id in net_ids:
            logger.info('========================================')
            logger.info('PROJECT={}, NETID={}'.format(project_id, net_id))
            grader = dockerGrader(project_id, net_id, logger)
            for test in grader.listTestScripts():
                grader.dockerRunSafe(test=test)

if __name__ == '__main__':
    main()
