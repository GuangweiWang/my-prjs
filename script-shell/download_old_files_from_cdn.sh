#!/bin/bash

#file_name_list=$1
#if [ "${file_name_list}x" == "x" ]; then echo "please input file_name list!"; exit 1; fi
file_name_list="DFW_OpenH265_objects.txt"

url_base="http://ciscobinary.openh264.org"
error_log="error.log"
echo "`date`" > $error_log

while read line
do
set -x
  file_name=`echo $line | awk -F "," '{print $1}'`
  file_size=`echo $line | awk -F "," '{print $2}'`
  file_url="${url_base}/${file_name}"

  curl -C - --retry 3 --retry-delay 60 -S -s -O $file_url
  if [ $? -ne 0 ]; then exit 1; fi
  file_actual_size=`ls -l $file_name | awk '{print $5}'`
set +x

  if [ "$file_actual_size" -ne "$file_size" ]; then
    echo "$file_name,$file_size,$file_actual_size" >> $error_log
  fi

done < $file_name_list

