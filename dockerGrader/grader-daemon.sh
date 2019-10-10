#!/bin/sh

#Adapted from https://stackoverflow.com/questions/3258243

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

run_grader() {
    echo "Running Auto-grader\n"

    echo "Auto-grader for P3:"
    python3 dockerUtil.py p3 ? -ff main.ipynb -x *.png -d ~/s3 -c

    echo "Auto-grader for P4:"
    python3 dockerUtil.py p4 ? -ff p4.py -x *.png -d ~/s3 -c

    echo "Auto-grader for P5:"
    python3 dockerUtil.py p5 ? -ff main.ipynb -x *.png -d ~/s3 -c
}

ntpdate -s time.nist.gov
git fetch

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
    run_grader
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    git pull
    run_grader
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
else
    echo "Diverged"
fi
