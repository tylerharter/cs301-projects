import argparse, boto3, botocore, csv, logging, requests, time

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

def sendRequests(ip, port, project, netIdList):
    for netId in netIdList:
        url = REQUEST_URL.format(ip=ip, port=port, project=project, netId=netId)
        logging.info("sending get request:" + url)
        response = requests.get(url)
        if response.status_code != 200:
            logging.warning(
                "Unexpected status code {} when requesting from {}".format(
                    response.status_code, url
                )
            )

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
        '--num_tasks',
        type=int,
        default=None,
        help='set the limit to the amount of tasks to grade (for debugging)')

    args = parser.parse_args()
    netIdList = getNetIdList(args.num_tasks)
    logging.info("Got {} netIds.".format(len(netIdList)))
    sendRequests(
        args.ip, args.port, args.project, netIdList)
    print("Success!")
