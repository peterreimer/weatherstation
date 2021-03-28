#/bin/bash
#gnuplot -e "DATA='$1'" wetter.plg

TIMESTAMP_LOG=`date "+%Y-%m-%dT%H:%M:%S"`

LOGS=~/git/weatherstation/plot/log
log_today=$LOGS/`date "+%Y/%m"`/`date "+%Y%m%d"`.csv
log_yesterday=$LOGS/`date -d "-1day" "+%Y/%m"`/`date -d "-1day" "+%Y%m%d"`.csv

echo $log_today
echo $log_yesterday

gnuplot -e "DATA='< cat $log_yesterday $log_today | tail -n 1440 '" wetter.plg