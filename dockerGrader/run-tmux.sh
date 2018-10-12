#!/bin/sh
export PATH="/home/vagrant/server/cs301-projects/dockerGrader:$PATH"
tmux new-session -d -s dockerGrader
tmux send-keys 'run-redis.sh' 'C-m'
tmux rename-window 'redis'
sleep 1
tmux split-window -t dockerGrader:0
tmux send-keys 'run-celery.sh' 'C-m'
tmux rename-window 'celery'
tmux split-window -h
tmux send-keys 'runDebug.sh' 'C-m'
tmux rename-window 'server'
tmux split-window -h -t 0
tmux send-keys 'run-flower.sh' 'C-m'
tmux rename-window 'run-flower.sh'
tmux -2 attach-session -t dockerGrader
