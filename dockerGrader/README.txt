The two files currently maintained:

1. Dockerfile: builds the Docker image named grader; you can see what students are given here
2. dockerUtil.py: runs student submissions (from S3) in Docker containers and uploads results (to S3)

Changes to dockerUtil:
*Refactored code into Classes because:
    -Enables use as a module (ex: for daemonizing)
    -Allows multiple instances to be ran simultaneously
    -Encapsulates vars for logging, stats collection, etc..
*Use argparse (stdlib) to better parse CLI arguments
*Use the official docker python SDK instead of subprocess (it's also faster!)
*Added some features:
    -Safe flag: runs grader without uploading results
    -Overwrite flag: re-runs all and overwrite's results in s3
    -Keepbest flag: re-run all but only update grade if better
    -S3dir flag: specify the s3 cached directory
    -Cleanup flag: remove s3 cache directory if set
*Copy over all files (except excluded) from project dir to code dir
    -Added exclude flag to specify which files not to copy
        -Accepts UNIX style file matching patterns
*Removed hard requirement on submission filename (for p4 to work)
*Added basic logging (more to come hopefully)
*Added some docstrings and more documentation
*PEP8-ified everything for better readability
*Removed some dependencies that weren't used
*Simplified s3 interface with use of pagination
*Added live, anonymous stats collection, dump pickle file to statsfile

TODO:
*Add logging with logfile and verbosity flag

