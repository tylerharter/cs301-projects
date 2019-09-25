# Standard libs
import os
import re
import json
import time
import base64
import shutil
import string
import argparse
from datetime import datetime

# Third party libs
import boto3
import docker


class Database:
    def __init__(self, s3dir='./s3', cleanup=False):
        self.BUCKET = 'caraza-harter-cs301'
        self.SEMESTER = "fall19"
        self.PROFILE = 'cs301ta'
        self.S3_DIR = os.path.abspath(s3dir)
        self.session = boto3.Session(profile_name=self.PROFILE)
        self.s3 = self.session.client('s3')
        self.safe_s3_chars = set(string.ascii_letters + string.digits + ".-_")
        self.cleanup = cleanup

    def get_submissions(self, project, rerun, email=None):
        prefix = 'a/projects/' + project + '/'
        if email:
            if '@' not in email:
                email += '@wisc.edu'
            prefix += self.to_s3_key_str(email) + '/'
        submitted = set()
        tested = set()
        for path in self.s3_all_keys(prefix):
            parts = path.split('/')
            if parts[-1] == 'submission.json':
                submitted.add(path)
            elif parts[-1] == 'test.json':
                parts[-1] = 'submission.json'
                tested.add('/'.join(parts))
        if not rerun:
            submitted -= tested
        return submitted

    def fetch_submission(self, s3path):
        local_dir = os.path.join(self.S3_DIR, os.path.dirname(s3path))
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        os.makedirs(local_dir)
        response = self.s3.get_object(Bucket=self.BUCKET, Key=s3path)
        submission = json.loads(response['Body'].read().decode('utf-8'))
        file_contents = base64.b64decode(submission.pop('payload'))
        file_name = submission['filename']
        # override the filename if it is a python source file
        if len(file_name) >= 3 and file_name.endswith('.py'):
            file_name = "main.py"
        elif len(file_name) >= 6 and file_name.endswith('.ipynb'):
            file_name = "main.ipynb"
        with open(os.path.join(local_dir, file_name), 'wb') as f:
            f.write(file_contents)
        return local_dir

    def fetch_results(self, s3path):
        s3path = s3path.replace('submission.json', 'test.json')
        response = self.s3.get_object(Bucket=self.BUCKET, Key=s3path)
        try:
            submission = json.loads(response['Body'].read().decode('utf-8'))
            return submission['score']
        except self.s3.exceptions.NoSuchKey:
            return 0

    def put_submission(self, key, submission):
        if type(submission) is not str:
            submission = json.dumps(submission, indent=2)
        self.s3.put_object(Bucket=self.BUCKET, Key=key,
                           Body=submission.encode('utf-8'),
                           ContentType='text/plain')

    def s3_all_keys(self, prefix):
        ls = self.s3.list_objects_v2(Bucket=self.BUCKET, Prefix=prefix, MaxKeys=10000)
        keys = []
        while True:
            print('...list_objects...')
            contents = [obj['Key'] for obj in ls.get('Contents', [])]
            keys.extend(contents)
            if 'NextContinuationToken' not in ls:
                break
            ls = self.s3.list_objects_v2(Bucket=self.BUCKET, Prefix=prefix, MaxKeys=10000,
                                         ContinuationToken=ls['NextContinuationToken'])
        return keys

    def to_s3_key_str(self, s):
        s3key = []
        for c in s:
            if c in self.safe_s3_chars:
                s3key.append(c)
            elif c == "@":
                s3key.append('*at*')
            else:
                s3key.append('*%d*' % ord(c))
        return "".join(s3key)

    def clear_caches(self):
        if self.cleanup and os.path.exists(self.S3_DIR):
            shutil.rmtree(self.S3_DIR)


class Grader(Database):
    def __init__(self, projects, netid, *args, safe=False, overwrite=False, keepbest=False, **kwargs):
        self.projects = projects
        self.netid = None if netid == '?' else netid
        self.safe = safe
        self.overwrite = overwrite
        self.keepbest = keepbest
        self.excluded_files = ['README.md', 'main.ipynb', 'main.py']
        super().__init__(*args, **kwargs)

    def run_test_in_docker(self, code_dir, image='grader',
                           cmd='python3 test.py', cwd='/code', timeout=60):
        shared_dir = {os.path.abspath(code_dir): {'bind': cwd, 'mode': 'rw'}}
        client = docker.from_env()

        # Run in docker container
        t0 = time.time()
        container = client.containers.run(image, cmd, detach=True,
                                          volumes=shared_dir, working_dir=cwd)
        print('CONTAINER', container.id)
        container.wait(timeout=timeout)
        t1 = time.time()

        # Get logs and remove container
        logs = self.parse_logs(container.logs())
        container.remove(v=True)

        # Get results
        try:
            with open(f'{code_dir}/result.json') as f:
                result = json.load(f)
        except Exception as e:
            result = {
                'score': 0,
                'error': str(e),
                'logs': logs.split("\n")
            }

        result['date'] = datetime.now().strftime("%m/%d/%Y")
        result['latency'] = t1 - t0
        return result

    @staticmethod
    def parse_logs(logs):
        # https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
        logs = logs.decode('ascii')
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', logs)

    def setup_codedir(self, project_dir, code_dir):
        for item in os.listdir(project_dir):
            item_path = os.path.join(project_dir, item)
            if item not in self.excluded_files and os.path.isfile(item_path):
                src = os.path.join(project_dir, item)
                dst = os.path.join(code_dir, item)
                shutil.copyfile(src, dst)

    def run_grader(self):
        for project_id in self.projects:
            submissions = self.get_submissions(project_id, rerun=self.overwrite or self.keepbest, email=self.netid)
            for s3path in sorted(submissions):
                print('========================================')
                print(s3path)

                # Setup environment
                code_dir = self.fetch_submission(s3path)
                project_dir = f'../{self.SEMESTER}/{project_id}/'
                self.setup_codedir(project_dir, code_dir)

                # Run tests in docker and save results
                result = self.run_test_in_docker(code_dir)
                new_score = result['score']
                print(f'Score: {new_score}')
                if not self.safe:
                    if self.keepbest and new_score < self.fetch_results(s3path):
                        print(f'Skipped {s3path} because better grade exists')
                    else:
                        self.put_submission('/'.join(s3path.split('/')[:-1] + ['test.json']), result)
                else:
                    print(f'Did not upload results, running in safe mode')
        self.clear_caches()


if __name__ == '__main__':
    extra_help = '\nTIP: run this if time is out of sync: sudo ntpdate -s time.nist.gov\n'
    parser = argparse.ArgumentParser(description='Auto-grader for CS301', epilog=extra_help)
    parser.add_argument('projects', type=str, nargs='+',
                        help='id(s) of project to run autograder on.')
    parser.add_argument('netid', type=str,
                        help='netid of student to run autograder on, or "?" for all students.')
    parser.add_argument('-safe', action='store_true', help='run grader without uploading results to s3.')
    parser.add_argument('-s3dir', type=str, help='directory of local s3 caches.')
    parser.add_argument('-cleanup', action='store_true', help='remove temporary s3 dir after execution')
    rerun_group = parser.add_mutually_exclusive_group()
    rerun_group.add_argument('-overwrite', action='store_true', help='rerun grader and overwrite any existing results.')
    rerun_group.add_argument('-keepbest', action='store_true', help='rerun grader, only update result if better.')

    grader_args = parser.parse_args()
    g = Grader(**vars(grader_args))
    g.run_grader()

