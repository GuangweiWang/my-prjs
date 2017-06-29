'''define following functions to call encoder and decoder for common use
    - wels_h264_encoder(infile,outfile,win,hin,wout,hout)
    - wels_h264_decoder(infile,outfile)
'''

import re
import subprocess
import config


WELS_H264ENC_EXE_PATH = config.TOOLS_PATH
WELS_H264DEC_EXE_PATH = config.TOOLS_PATH

#TODO: add more args
def wels_h264_encoder(infile, outfile, win, hin, wout, hout,
                      rc=-1, qp=26, usage_type=0, layer_num=1):
    '''
    this function uses to call wels h264encoder.

    usage:
        wels_h264_encoder(infile.yuv, outfile.264, win, hin, wout, hout)

    parameters:
        infile.yuv      the input file to be encoded
        outfile.264     the output file(.264 format)
        win             width of original file
        hin             height of original file
        wout            width of output file
        hout            height of output file

    return:
        frames          total frame number encoded
        encoder_time    total encoding time
        fps             FPS
        downsample_time time cost of down sample

    '''

    encoder = WELS_H264ENC_EXE_PATH + 'h264enc'
    encoder_cfg = config.H264CFG_PATH + 'welsenc.cfg'
    encoder_layer_cfg = config.H264CFG_PATH + 'layer2.cfg'

    cmdline = str('%s %s -lconfig 0 %s '
                  '-bf %s -org %s -rc -1 '
                  '-sw %d -sh %d -dw 0 %d -dh 0 %d'
                  % (encoder, encoder_cfg, encoder_layer_cfg,
                     outfile, infile,
                     win, hin, wout, hout))
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE)
    result_line = p.communicate()[0]

    frames = 0
    re_frames = re.compile(r'Frames:		(\d+)\n')
    r = re_frames.search(result_line)
    if r is not None:
        frames = float(r.groups()[0])

    fps = 0
    re_fps = re.compile(r'FPS:\t\t(\d+.\d+) fps\n')
    r = re_fps.search(result_line)
    if r is not None:
        fps = float(r.groups()[0])

    encoder_time = 0
    re_encoder_time = re.compile(r'encode time:\t(\d+.\d+) sec\n')
    r = re_encoder_time.search(result_line)
    if r is not None:
        encoder_time = float(r.groups()[0])

    downsample_time = 0
    re_downsample_time = re.compile(r'down sample time: (\d+.\d+) sec\n')
    r = re_downsample_time.search(result_line)
    if r is not None:
        downsample_time = float(r.groups()[0])

    return frames, encoder_time, fps, downsample_time

#TODO: return decoder time
def wels_h264_decoder(infile, outfile):
    '''
    this function uses to call wels h264decoder

    usage:
        wels_h264_decoder(infile.264, outfile.yuv)

    parameters:
        infile.264      input file to be decoded
        outfile.yuv     output yuv file(I420 format)

    return:
        decode_time     total decoding time
        frames          frame number decoded
    '''

    decoder = WELS_H264DEC_EXE_PATH + 'h264dec'

    cmdline = str('%s %s %s' % (decoder, infile, outfile))
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result_line = p.communicate()[1]
    print(result_line)

    #decode_frames = 0
    decode_time = 0
    re_decode_time = re.compile(r'decode time:\t(\d+.\d+) sec\n')
    r = re_decode_time.search(result_line)
    if r is not None:
        decode_time = float(r.groups()[0])

    return decode_time
