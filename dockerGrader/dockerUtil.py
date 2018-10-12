import base64, boto3, botocore, os, sys, json, subprocess, shutil, time, traceback

ACCESS_KEY = "projects/{project}/users/{googleid}/curr.json"
GOOGLE_KEY = "users/net_id_to_google/{netid}.txt"
UPLOAD_KEY = "ta/grading/{project}/{netid}.json"
TEST_DIR = "/tmp/test/{netId}"
SUBMISSIONS = 'submissions'
BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

class dockerGrader:
    def __init__(self, project, netid, logger):
        self.project = project
        self.netid = netid
        self.containerid = None

        self.submissionKey = ACCESS_KEY.format(project=self.project, googleid=self.googleid)
        self.googleKey = GOOGLE_KEY.format(netid=self.netid)
        self.uploadKey = UPLOAD_KEY.format(project=self.project, netid=self.netid)

        self.testDir = TEST_DIR.format(netid=netid)

        self.currentUID = getCurrentUID()
        self.googleid = self.lookupGoogleId()

    # Util Functions
    def getCurrentUID(self):
        userName = os.environ.get("USER")
        if not userName:
            self.logger.warning("Invalid userName.")
        r = int(subprocess.check_output(["id", "-u", userName]))
        logger.info("current user: {}, current uid: {}".format(userName, r))
        return r

    def lookupGoogleId(self):
        try:
            response = s3.get_object(Bucket=BUCKET, Key=self.googleKey)
            netid = response['Body'].read().decode('utf-8')
            return netid
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
        exitCode, isRunning = self.containerStatus(self.containerId)
        if isRunning:
            if hardLimit:
                self.uploadResult({"score":0, "error":"Timeout"})
                self.logger.info("project: {}, netid: {}, timeout".format(
                    self.project, self.netId))
            else:
                self.logger.info("project: {}, netid: {}, soft limit check failed.".format(
                    self.project, self.netId))
                return True
        elif exitCode:
            self.uploadResult({"score":0, "error":"ExitCode:" + str(exitCode)})
            self.logger.info("project: {}, netid: {}, exit with {}".format(
            self.project, self.netId, exitCode))
        else:
            self.uploadResult()
            self.logger.info("project: {}, netid: {}, docker exit normally".format(
                self.project, self.netId))
        return False

    def rmContainer(self):
        forceRmCmd = ["docker", "rm", "-f", self.containerId]
        try:
            subprocess.check_output(forceKillCmd)
        except:
            self.logger.info("rm cantainer failed. ID: {}".format(self.containerId))

    # Main Functions
    def dockerRun(self):
        # create directory to mount inside a docker container
        if os.path.exists(seld.testDir):
            shutil.rmtree(seld.testDir)
        os.makedirs(seld.testDir)
        self.downloadSubmission()

        # we can't use shutil.copytree here again because TEST_DIR exists
        testCodePath = "./test/{}".format(self.project)
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
               '-v', os.path.abspath(self.testDir)+':/code',  # share the test dir inside
               '-u', str(self.currentUID),                     # run as local user (instead of root)
               '-w', '/code',                             # working dir is w/ code
               image,                                     # what docker image?
               'python3', 'test.py']                      # command to run inside
        self.containerId = subprocess.check_output(cmd).decode("ascii").replace("\n","")
        self.logger.info("docker cmd:" + ' '.join(cmd))
        self.logger.info("container id:" + self.containerId)
        time.sleep(2)
        if self.dockerLiveCheck():
            time.sleep(5)
            self.dockerLiveCheck(hardLimit = True)
        self.rmContainer()
