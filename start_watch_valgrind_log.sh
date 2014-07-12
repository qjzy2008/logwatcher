#!/bin/bash
PID=`ps -ef |grep "python watch_valgrind_log.py" |grep -v grep | awk '{print $2}'`
if [ "$PID" != "" ]; then
echo "logwatcher is runing!"
exit
fi
echo "python watch_valgrind_log.py &"
python watch_valgrind_log.py &
