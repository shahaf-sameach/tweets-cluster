#!/bin/bash

while true; 
do
  sh /home/ir/sameacs/tweets-cluster/cron/live_stream_watchdog.sh >> /home/ir/sameacs/tweets-cluster/logs/watchdog.log 2>&1
  sh /home/ir/sameacs/tweets-cluster/cron/ids_stream_watchdog.sh >> /home/ir/sameacs/tweets-cluster/logs/watchdog.log 2>&1
  sleep 1m
done
