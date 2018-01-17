#!/bin/bash

mkdir -p "/home/ir/sameacs/tweets-cluster/pids"
PIDFILE="/home/ir/sameacs/tweets-cluster/pids/ids_stream.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= |
                           grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
  echo "Stream by ids Already running."
  exit 99
fi

echo "Starting Stream by ids..."
python /home/ir/sameacs/tweets-cluster/stream_by_ids.py >> /home/ir/sameacs/tweets-cluster/logs/ids_stream.log 2>&1 &

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"