import os, sys, re, subprocess, glob
import config

DOWN_CONVERT_PATH = config.TOOLS_PATH
DOWN_SAMPLER_PATH = config.TOOLS_PATH
IMAGE_PROCESS_PATH = config.TOOLS_PATH

H264ENC_PATH = config.TOOLS_PATH
H264DEC_PATH = config.TOOLS_PATH
H264CFG_PATH = config.TOOLS_PATH



#wels sharpen
def image_process(width, height, infile, outfile, method=0):
  imageProcess = IMAGE_PROCESS_PATH + 'imageProcess.bin'

  cmdline = str('%s %s %s %s %s -method %d' %(imageProcess, width, height, infile, outfile, method))
  p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE)
  result_line = p.communicate()[0]
  #print result_line

  total_time = frame_time = 0
  re_time = re.compile(r'Total Time:     (\d+.\d*) sec => (\d+.\d*) ms/f')
  r = re_time.search(result_line)

  if r is not None:
    total_time = float(r.groups()[0])
    frame_time = float(r.groups()[1])

  return total_time, frame_time




#caculate PSNR
def PSNRStaticd(width, height, original, rec, output_name=None, bs_name=None, frame_rate=None):
    psnr_path = PSNR_PATH

    if bs_name and frame_rate:
        cmdline = str('%sPSNRStaticd %d %d %s %s 0 0 %s %d Summary -r '
                    % (psnr_path+ os.sep, width, height, original, rec, bs_name, frame_rate))
    else:
        cmdline = str('%sPSNRStaticd %d %d %s %s Summary -r '
                    % (psnr_path+ os.sep, width, height, original, rec))
    if output_name:
        cmdline += ' 1> %s.log' %(output_name)

    p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result_line = p.communicate()[1]

    #'0,43.5978,45.7192,46.5856, 1,43.5547,45.7233,46.4990, 2,43.4785,45.6879,46.4916
    # #Summary,bitrate (kbps):,49107.2000,total PSNR:,43.5437,45.7102,46.5254
    frame_num = 0
    match_re_last_frame = re.compile(r'(\d+),\d+.\d+,\d+.\d+,\d+.\d+\n\nSummary')
    r = match_re_last_frame.search(result_line)
    if r is not None:
        frame_num = int(r.group(1))+1
    match_re_last_frame = re.compile(r'(\d+),\d+.\d+,\d+.\d+,\d+.\d+\n\ntotal PSNR')
    r = match_re_last_frame.search(result_line)
    if r is not None:
        frame_num = int(r.group(1))+1


    match_re_psnr = re.compile(r'Summary,bitrate \(kbps\):,(\d+.\d+),total PSNR:,(\d+.\d+),(\d+.\d+),(\d+.\d+)')
    r = match_re_psnr.search(result_line)
    if r is not None:
        return frame_num, float(r.group(1)), float(r.group(2)), float(r.group(3)), float(r.group(4))

    #    total PSNR:,33.0557,46.5008,40.4059
    match_re_psnr = re.compile(r'total PSNR:,(\d+.\d+),(\d+.\d+),(\d+.\d+)')
    r = match_re_psnr.search(result_line)
    if r is not None:
        return frame_num, 0, float(r.group(1)), float(r.group(2)), float(r.group(3))

    return 0, 0, 0, 0, 0

#get resolution by file name
def get_resolution_from_name(f):
    resolution_re = re.compile(r'(\d+)x(\d+)_(\d+)')
    r = resolution_re.search(f)
    if r is not None:
        width = int(r.group(1))
        height = int(r.group(2))
        framerate = int(r.group(3))
        return width, height, framerate

    resolution_re2 = re.compile(r'(\d+)x(\d+)')
    r = resolution_re2.search(f)
    if r is not None:
        width = int(r.group(1))
        height = int(r.group(2))
        return width, height, 30

    return 0, 0, 0

def process(one_yuv, sequence_type, downscale=2):
  print 'processing ', one_yuv
  out_path = OUT_DATA_PATH
  infile_name = os.path.basename(one_yuv)

  src_width, src_height, frame_rate = get_resolution_from_name(infile_name)
  dst_width = src_width / downscale;
  dst_height = src_height / downscale;
  resolution_in = '%dx%d' %(src_width, src_height)
  resolution_out = '%dx%d' %(dst_width, dst_height)

  loop_list = ['_jsvm', '_bilinear', '_bilinear_sharpen','_bicubic','_tap6', '_tap8', '_hybrid']

  for suffix in loop_list:
    log_name = out_path + 'Test_downsampler_compare_' + sequence_type + suffix + '.csv'
    flog = open(log_name, 'ab')

    out_name = out_path + infile_name[0:-4] + '_to_' + resolution_out + suffix + '.yuv'
    bs_name = out_name[0:-4] + '.264'
    rec_name = out_name[0:-4] + '_rec.yuv'

    print 'down sampling ...\n'
    if suffix == '_jsvm':
      dt, ft = DownConvert(src_width, src_height, one_yuv, dst_width, dst_height, out_name)
    elif suffix == '_bilinear_sharpen':
      out_name_temp = out_name[0:-4] + '_tmp.yuv'
      dt, ft = downsampler(src_width, src_height, one_yuv, dst_width, dst_height, out_name_temp, 0)
      dt1, ft1 = image_process(dst_width, dst_height, out_name_temp, out_name, 0)
      os.remove(out_name_temp)
      dt = dt + dt1
      ft = ft + ft1
    elif suffix == '_bilinear':
      dt, ft = downsampler(src_width, src_height, one_yuv, dst_width, dst_height, out_name, 0)
    elif suffix == '_bicubic':
        dt, ft = downsampler(src_width, src_height, one_yuv, dst_width, dst_height, out_name, 2)
    elif suffix == '_tap6':
      dt, ft = downsampler(src_width, src_height, one_yuv, dst_width, dst_height, out_name, 4)
    elif suffix == '_tap8':
      dt, ft = downsampler(src_width, src_height, one_yuv, dst_width, dst_height, out_name, 1)
    elif suffix == '_hybrid':
      dt, ft = downsampler(src_width, src_height, one_yuv, dst_width, dst_height, out_name, 3)
    else:
      dt, ft = 0, 0

    print 'encoding ...\n'
    frame_num, enc_time, fps = h264enc(bs_name, out_name, dst_width, dst_height, dst_width, dst_height)
    bs_size = os.path.getsize(bs_name)
    print 'decoding ... \n'
    dec_time = h264dec(bs_name, rec_name)
    print 'caculate PSNR ... \n'
    frames, bitrate, psnry, psnru, psnrv = PSNRStaticd(dst_width, dst_height, out_name, rec_name)

    os.remove(out_name)
    os.remove(bs_name)
    os.remove(rec_name)

    flog.write('%s,%s,%s,%s,'
               '%f,%f,'
               '%f,%f,%f,%f,'
               '%f,%f,%f,\n'
               %(infile_name, resolution_in, resolution_out, frame_num, dt, ft, enc_time, fps, bs_size, dec_time, psnry, psnru, psnrv))
    flog.close()



if __name__ == '__main__':
  out_path = OUT_DATA_PATH

  sequence_type = 'screen'
  sequence_path = SCREEN_SEQUENCES_PATH

  downscale = 2

  yuv_list = []
  for f in glob.glob(sequence_path + '*.yuv'):
    yuv_list.append(f)

  loop_list = ['_jsvm', '_bilinear', '_bilinear_sharpen','_bicubic','_tap6', '_tap8', '_hybrid']
  for suffix in loop_list:
    log_name = out_path + 'Test_downsampler_compare_' + sequence_type + suffix + '.csv'
    flog = open(log_name, 'wb')
    flog.write('FileName, SrcResolution, DstResolution, FrameNum,'
               'DownTimeTotal, DowntimeFrame,'
               'EncTime, Fps, BitstreamSize, DecTime,'
               'PSNRy,PSNRu, PSNRv\n')
    flog.close()

  for one_yuv in yuv_list:
    process(one_yuv, sequence_type, downscale)








