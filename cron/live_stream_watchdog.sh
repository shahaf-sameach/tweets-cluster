#!/bin/bash

mkdir -p "/home/ir/sameacs/tweets-cluster/pids"
PIDFILE="/home/ir/sameacs/tweets-cluster/pids/live_stream.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= |
                           grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
  echo "Live Stream Already running."
  exit 99
fi

echo "Starting Live Stream..."
source /home/ir/sameacs/.venv/bin/activate
python /home/ir/sameacs/tweets-cluster/stream/live_stream.py >> /home/ir/sameacs/tweets-cluster/logs/live_stream.log 2>&1 &

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"
