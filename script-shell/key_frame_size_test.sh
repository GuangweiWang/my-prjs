#!/bin/bash
current_dir=`pwd`

#********** parameter settings **********#
enc_cfg="$HOME/Workspace/config/welsenc.cfg"
layer_cfg="$HOME/Workspace/config/layer2.cfg"
enc_exe="$HOME/Workspace/openh264/h264enc"

src_dir="$HOME/Workspace/video/yuv/scc"
src_file="Doc_BJUT_1280x720.yuv"

result_file="key_frame_size_test_""`date +%Y%m%d`"".csv"
log_file="trace.log"


#encoder parameters
qp_list="18 19 20 22 23 24 27 28 29"
#********** parameter settings **********#

#parse input arg
while [ $# -gt 0 ]; do
case $1 in 
    -sdir)
	        shift
	        src_dir="$1"
	        shift
	        ;;
	-sfile)
	        shift
	        src_file="$1"
	        shift
	        ;;
	*)
	        echo "Error:invalid arg: $1"
	        exit 1
	        ;;
esac
done


#set src files
if [ "${src_file}x" != "x" ]; then
file_dir=`dirname $src_file `
file_name=`basename $src_file `
if [ "${file_dir}" != "." ] ; then src_dir="$file_dir" ;fi
if [ "${file_dir}" == "." ] && [[ "${src_file}" =~ "./" ]] ; then src_dir="." ;fi
src_file=$file_name

yuv_seqs="${src_dir}/${src_file}"
else
yuv_seqs=`ls ${src_dir}/*.yuv`
fi
echo "yuv_seqs=$yuv_seqs"

#wirte headline on resulte file
echo "yuv_name,resolution,qp,key_frame_size" > $result_file
#echo "test on: `uname -s`, `uname -m`" > $log_file


#encoding yuvs and testing
for one_yuv in ${yuv_seqs}
do
file_name=`basename $one_yuv `
file_dir=`dirname $one_yuv `
resolution=`echo $file_name | grep -o "[0-9]\+x[0-9]\+" `
src_width=`echo $resolution | awk -F "x" '{print $1}' `
src_height=`echo $resolution | awk -F "x" '{print $2}' `

for one_qb in ${qp_list}
do
cmd="$enc_exe $enc_cfg -lconfig 0 $layer_cfg -org $one_yuv -bs test.264 -sw $src_width -sh $src_height -dw 0 $src_width -dh 0 $src_height -trace 15"

$cmd > $log_file 2>&1
done

done






