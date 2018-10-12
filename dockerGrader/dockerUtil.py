import base64, boto3, botocore, os, sys, json, subprocess, shutil, time, traceback

ACCESS_KEY = "projects/{project}/users/{googleId}/curr.json"
GOOGLE_KEY = "users/net_id_to_google/{netId}.txt"
UPLOAD_KEY = "ta/grading/{project}/{netId}.json"
TEST_DIR = "/tmp/test/{netId}"
SUBMISSIONS = 'submissions'
BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

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

    # Download Functions
    def downloadSubmission(self):
        if not self.googleId:
            return
        # a project path will look something like this:
        # projects/p0/users/115799594197844895033/curr.json
        self.logger.info('downloading to {}'.format(self.testDir))
        # download
        response = s3.get_object(Bucket=BUCKET, Key=self.submissionKey)
        submission = json.loads(response['Body'].read().decode('utf-8'))
        fileContents = base64.b64decode(submission.pop('payload'))
        fileName = submission['filename']
        # override the filename if it is a python source file
        if len(fileName) >= 3 and fileName[-2:] == 'py':
            fileName = "main.py"
        with open(os.path.join(self.testDir, fileName), 'wb') as f:
            f.write(fileContents)

    # Upload Functions
    def uploadResult(self, errorLog = None):
        if errorLog:
            serializedResult = json.dumps(errorLog)
        else:
            try:
                with open("{}/result.json".format(self.testDir), "r") as fr:
                    serializedResult = fr.read()
            except:
                serializedResult = json.dumps({"score":0, "error": "result not found"})
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

    # Main Functions
    def dockerRun(self):
        # create directory to mount inside a docker container
        if os.path.exists(self.testDir):
            shutil.rmtree(self.testDir)
        os.makedirs(self.testDir)
        self.downloadSubmission()

        # we can't use shutil.copytree here again because TEST_DIR exists
        testCodePath = "./test/{}".format(self.project)
        for item in os.listdir(testCodePath):
            src = os.path.join(testCodePath, item)
            dest = os.path.join(self.testDir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)

        # run tests inside a docker container
        image = 'python:3.7-stretch' # TODO: find/build some anaconda image
        cmd = ['docker', 'run',                           # start a container
               '-d',                                      # detach mode
               '--rm',                                    # remove the container when exit
               '-v', os.path.abspath(self.testDir)+':/code',  # share the test dir inside
               '-u', str(self.currentUID),                     # run as local user (instead of root)
               '-w', '/code',                             # working dir is w/ code
               image,                                     # what docker image?
               'python3', 'test.py']                      # command to run inside
        self.containerId = subprocess.check_output(cmd).decode("ascii").replace("\n","")
        self.logger.info("docker cmd:" + ' '.join(cmd))
        self.logger.info("container id:" + self.containerId)
        time.sleep(8)
        if self.dockerLiveCheck():
            time.sleep(20)
            self.dockerLiveCheck(hardLimit = True)
        self.rmContainer()
