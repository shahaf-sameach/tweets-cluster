#!/bin/bash

mkdir -p "/home/ir/sameacs/tweets-cluster/pids"
PIDFILE="/home/ir/sameacs/tweets-cluster/pids/ids_stream.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= |
                           grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
  echo "$(date '+%d/%m/%Y %H:%M:%S') Stream by ids Already running."
  exit 99
fi

echo "$(date '+%d/%m/%Y %H:%M:%S') Starting Stream by ids..."
source /home/ir/sameacs/.venv/bin/activate
export PYTHONPATH=/home/ir/sameacs/tweets-cluster
python -u /home/ir/sameacs/tweets-cluster/stream/file_stream.py >> /home/ir/sameacs/tweets-cluster/logs/file_stream.log 2>&1 &

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"
