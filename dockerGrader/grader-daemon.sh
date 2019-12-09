#!/bin/sh

#Adapted from https://stackoverflow.com/questions/3258243

cd $(dirname "$0")

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

PY=/nobackup/cs301-pyenv/bin/python3


run_grader() {
    export AWS_SHARED_CREDENTIALS_FILE="/nobackup/.aws/credentials"

    echo "Running Auto-grader\n"

    echo "\n\nAuto-grader for p10:"
    $PY dockerUtil.py p10 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p9:"
    $PY dockerUtil.py p9 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p8:"
    $PY dockerUtil.py p8 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p7:"
    $PY dockerUtil.py p7 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for P6:"
    $PY dockerUtil.py p6 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for P5:"
    $PY dockerUtil.py p5 ? -ff main.ipynb -x *.png -c

    echo "\n\nAuto-grader for P4:"
    $PY dockerUtil.py p4 ? -ff p4.py -x *.png -c

    echo "\n\nAuto-grader for P3:"
    $PY dockerUtil.py p3 ? -ff main.ipynb -x *.png -c
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
