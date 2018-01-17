#!/bin/bash

mkdir -p "/home/ir/sameacs/tweets-cluster/pids"
PIDFILE="/home/ir/sameacs/tweets-cluster/pids/live_stream.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= |
                           grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
  echo "Already running."
  exit 99
fi

python /home/ir/sameacs/tweets-cluster/live_stream.py >> /home/ir/sameacs/tweets-cluster/logs/live_stream.log 2>&1 &

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"