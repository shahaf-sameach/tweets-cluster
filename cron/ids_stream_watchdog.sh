#!/bin/bash

mkdir -p "/home/ir/sameacs/tweets-cluster/pids"
PIDFILE="/home/ir/sameacs/tweets-cluster/pids/ids_stream.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= |
                           grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
  echo "Stream by ids Already running."
  exit 99
fi

echo "Starting Stream by ids..."
source /home/ir/sameacs/.venv/bin/activate
export PYTHONPATH=/home/ir/sameacs/tweets-cluster
python /home/ir/sameacs/tweets-cluster/stream/file_stream.py >> /home/ir/sameacs/tweets-cluster/logs/file_stream.log 2>&1 &

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"
