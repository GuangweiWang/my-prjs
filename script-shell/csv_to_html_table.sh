#!/bin/bash

usage="usage: `basename $0` <-i|--input inputfile.csv> <-o|--output outputfile.html>"

#parse arg
while [ $# -gt 0 ]; do
case $1 in
  -i|--input)
    input_file=$2
	shift; shift
	;;
  -o|--output)
    output_file=$2
	shift; shift
	;;
  *)
    echo $usage
	exit 1
	;;
esac
done

#
if [ "${input_file}x" == "x" ]; then echo $usage && exit 1 ;fi
if [ "${output_file}x" == "x" ]; then echo $usage && exit 1 ;fi

#
echo "<html>" > $output_file
echo '<table border="1">' >> $output_file

while read line
do
  echo "<tr>" >> $output_file
  out_line=`echo $line | sed "s;,;</th><th>;g" | sed "s;^;<th>&;" | sed "s;$;</th>&;"`
  echo $out_line >> $output_file
  echo "</tr>" >> $output_file
done < $input_file


echo "</table>" >> $output_file
echo "</html>" >> $output_file

