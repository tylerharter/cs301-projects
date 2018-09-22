import argparse, boto3, botocore, csv, math, logging, requests, threading, time, json

REQUEST_URL="http://{ip}:{port}/json/{project}/{netId}"
RESULT_PATH="ta/grading/{project}/{netId}.json"
CUR_SUBMISSION_PATH="projects/{project}/users/{googleId}/curr.json"
SUBMISSIONS = 'submissions'
BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

logging.basicConfig(
    handlers=[
        logging.FileHandler("dockerGraderClient.log"),
        logging.StreamHandler()
    ],
    level=logging.INFO)

# return all S3 objects with the given key prefix, using as many
# requests as necessary
def s3_all_keys(Prefix):
    ls = s3.list_objects_v2(Bucket=BUCKET, Prefix=Prefix, MaxKeys=10000)
    keys = []
    while True:
        contents = [obj['Key'] for obj in ls.get('Contents',[])]
        keys.extend(contents)
        if not 'NextContinuationToken' in ls:
            break
        ls = s3.list_objects_v2(Bucket=BUCKET,
                                Prefix=Prefix,
                                ContinuationToken=ls['NextContinuationToken'],
                                MaxKeys=10000)
    return keys

def getNetIdList(numTasks):
    keys = s3_all_keys("users/net_id_to_google")
    # convert from the full path to file name and remove txt suffix.
    processedKeys = [key[key.rfind("/") + 1: -4] for key in keys]
    limit = min(numTasks, len(processedKeys)) if numTasks else len(processedKeys)
    return processedKeys[:limit]

def sendRequests(ip, port, project, netIdList, numContainers):
    counter = 0
    for netId in netIdList:
        counter += 1
        url = REQUEST_URL.format(ip=ip, port=port, project=project, netId=netId)
        logging.info("sending get request:" + url)
        response = requests.get(url)
        if response.status_code != 200:
            logging.warning(
                "Unexpected status code {} when requesting from {}".format(
                    response.status_code, url
                )
            )
        if counter >= numContainers:
            counter = 0
            logging.info("wait for the completion.")
            time.sleep(3)

# General template to fetch from s3
def s3Fetcher(path, name, raiseError = True):
    try:
        response = s3.get_object(Bucket=BUCKET, Key=path)
        return response['Body'].read().decode('utf-8')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            logging.info(
                "key {} doesn't exist when look up for {}.".format(path, name))
        else:
            logging.warning(
                "Unexpected error {} when look up for {}.".format(e.response['Error']['Code'], name))
            if raiseError:
                raise e

def lookupGoogleId(netId):
    path = 'users/net_id_to_google/%s.txt' % netId
    return s3Fetcher(path, "Google ID", False)

def getMetadataInfoJson(netId, project):
    googleId = lookupGoogleId(netId)
    metadataPath = CUR_SUBMISSION_PATH.format(googleId=googleId, project=project)
    response = s3Fetcher(metadataPath, "Metadata Info", False)
    return json.loads(response)

def downloadGrade(netIdList, project):
    gradeInfo = []
    for netId in netIdList:
        resultPath = RESULT_PATH.format(project=project, netId=netId)
        response = s3Fetcher(resultPath, "Grade Result", False)
        if not response:
            gradeInfo.append((netId, 0, "Result not found", -1, ""))
            continue

        gradeJson = json.loads(response)
        grade = gradeJson.get("score", 0)
        errorReason = gradeJson.get("error")
        partnerId = gradeJson.get("partner_netid")
        metadataInfo = getMetadataInfoJson(netId, project)

        if "score" not in gradeJson:
            logging.warning("Invalid result. json file fetched for netId: {}".format(netId))
        lateDays = metadataInfo.get("late_days", 0) if metadataInfo else -1
        intLateDays = 0 if lateDays <= 0 else math.ceil(lateDays)
        logging.info("netId: {} processed. grade: {} {} late days: {}".format(
            netId,
            grade,
            "Error: {}".format(errorReason) if errorReason else "",
            lateDays))
        gradeInfo.append((netId, grade, errorReason, intLateDays, partnerId))
    return gradeInfo

def generateCsv(gradeInfo, saveFileName):
    with open(saveFileName, "w") as csvfw:
        csvWriter = csv.writer(csvfw)
        for row in gradeInfo:
            csvWriter.writerow(row)
    print("Successfully generated csv file " + saveFileName)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send batch requests to dockerGrader')

    parser.add_argument(
        '-i',
        '--ip',
        default="127.0.0.1",
        help='set dockerGrader server ip')
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='set dockerGrader server port')
    parser.add_argument(
        '-p',
        '--project',
        required=True,
        help='set dockerGrader server grading project')
    parser.add_argument(
        '-n',
        '--num_containers',
        type=int,
        default=2,
        help='number of docker containers to run at the same time')
    parser.add_argument(
        '--num_tasks',
        type=int,
        default=None,
        help='set the limit to the amount of tasks to grade (for debugging)')

    args = parser.parse_args()
    netIdList = getNetIdList(args.num_tasks)
    logging.info("Got {} netIds.".format(len(netIdList)))
    sendRequests(
        args.ip, args.port, args.project, netIdList, args.num_containers)
    print("Waiting for the completion of grading container", end="")
    for i in range(5):
        time.sleep(1)
        print("...")
    pause = input("Press any key to continue. Please make sure all docker tasks finished.")
    gradeInfo = downloadGrade(netIdList, args.project)
    generateCsv(gradeInfo, "{}_{}.csv".format(
        args.project, time.strftime("%m%d_%H%M", time.gmtime(time.time()))))
