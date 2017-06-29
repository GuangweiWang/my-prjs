"test down sample"

import os,datetime
import tools_downsampler, tools_common, tools_codec, config


def compare_bilinear_jsvm(test_seq_path, out_result_path):
    '''
    this function use to compare bilinear and jsvm down sample modules

    usage:
        compare_bilinear_jsvm(test_seq_path, out_result_path)

    parameters:
        - test_seq_path:      the path of test sequences
        - out_result_path:    the path yout want to save the result .csv file on

    returns:
        no parameters
    '''


    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.datetime.now().strftime("%H:%M:%S")

    #
    down_sample_type = 'jsvm'
    simulcast = 'simulcast'

    #save following result in .csv file, b:bilinear; j:jsvm
    result_file = open(out_result_path + 'compare_downsample_%s.csv' %date_now, 'a')
    result_file.write('%s, %s\n' %(down_sample_type, simulcast))
    result_file.write('down_sampler,filename,frames,src_resolution,dst_resolution,'
                      'encode_time,fps,downsample_time,bitstream_size,psnr_y,psnr_u,psnr_v,\n')

    #get all test sequence
    #all_sequences = glob.glob(test_seq_path + '*.yuv')
    all_sequences = [test_seq_path + 'Mac_Camera_0x106B_Back_Light_Terrible_Head_Shoulder_1280x720_30FPS_I420.yuv',
                     test_seq_path + 'Mac_Camera_0x106B_Move_One_1280x720_30FPS_I420.yuv',
                     test_seq_path + 'iphone5A1429_walking_720x1280.yuv']
    all_downscale = [2, 4, 8]

    package_name = out_file_path + 'downsample_encoder_output_yuvs_%s.tar' %date_now

    if os.path.isfile(package_name):
        pass
    else:
        readme_name = out_file_path + 'README'
        file_readme = open(readme_name, 'w')
        file_readme.write('by guangwei %s %s\n' %(date_now, time_now))
        file_readme.write('to save down sample and codec rec yuv file\n')
        file_readme.close()
        os.system('tar -cvf %s %s' %(package_name, readme_name))

    for sequence in all_sequences:
        pass #todo
        #step 1: encode sequence, get encode_time, fps, down_sample_time, bitstream_size
        #setp 2: use DownConvert or down_sample tool down sampel src resolution to dst one
        #step 3: calculate PSNR about the result of DownConvert/down_sample and encoder+decoder
        #setp 4: save psnr

        print('processing %s' %sequence)
        for down_scale in all_downscale:
            src_width, src_height, frame_rate = tools_common.get_resolution_from_file_name(sequence)
            dst_width = src_width / down_scale
            dst_height = src_height/ down_scale

            file_name = os.path.basename(sequence)
            bitstream = out_result_path + file_name[0:-4] + \
                        '_to_%dx%d' %(dst_width, dst_height) + '_%s' %down_sample_type + '_%s' %simulcast + '.264'
            rec_yuv = bitstream[0:-4] + '_rec.yuv'
            down_sample_yuv = bitstream[0:-4] + '.yuv'

            frames, encode_time, fps, downsample_time = tools_codec.wels_h264_encoder(
                sequence, bitstream,src_width, src_height, dst_width, dst_height)
            tools_codec.wels_h264_decoder(bitstream, rec_yuv)
            if down_sample_type == 'bilinear':
                tools_downsampler.wels_downsampler(
                    src_width, src_height, sequence, dst_width, dst_height, down_sample_yuv)
            else:
                tools_downsampler.jsvm_down_convert(
                    src_width, src_height, sequence, dst_width, dst_height, down_sample_yuv)

            fn, br, psnr_y, psnr_u, psnr_v = tools_common.calculate_PSNR_staticd(
                dst_width, dst_height, down_sample_yuv, rec_yuv)
            bitstream_size = os.path.getsize(bitstream)

            result_file.write('bilinear,%s,%d,%sx%s,%sx%s,'
                                  '%f,%f,%f,%d,%f,%f,%f,\n'
                                  %(file_name, frames, src_width, src_height, dst_width, dst_height,
                                    encode_time, fps, downsample_time, bitstream_size, psnr_y, psnr_u, psnr_v))

            os.system('tar -rvf %s %s' %(package_name, rec_yuv))
            os.system('tar -rvf %s %s' %(package_name, down_sample_yuv))
            os.remove(bitstream)
            os.remove(rec_yuv)
            os.remove(down_sample_yuv)

    result_file.close()


def compare_diff_tap_filter(test_seq_path, out_result_path):
    '''
    description:
        -this funtion to compare two bilinear tap-filter down-samplers.this two filter are very similar, one is
        accurately the same as dyadic-bilinear down-sampler, another calculate average value of 16-tap(1:4) or
        64-tap(1:8) for the target pixel.

    process steps & data flow:

    :param test_seq_path:
    :param out_result_path:
    :return:
    '''


def test_downsampler(test_seq_path, out_result_path):
    '''
    description:
        -this function to compare down_sampler.bin(dyadic bilinear filter and tap-filter bilinear) to DownConvert;
        -Mar.30,2016; @cisco; Hefei
        -Guangwei

    process steps & data flow:
        1. source.yuv           -> downsampler      -> down_sampled.yuv
        2. down_sampled.yuv     -> h264enc          -> bit_stream.264
        3. bit_stream.264       -> h264dec          -> rec_file.yuv
        4. down_sampled.yuv &
           rec_file.yuv         -> PSNRStatic       -> psnr result
        5. compare different down-sampler results and save results

    usage:
        test_downsampler(test_seq_path, out_result_path)

    parameters:
        -test_seq_path:     path of the origin test sequences
        -out_result_path:   path of out result files, e.g. *.yuv *.csv ...

    returns:
        none,
        but save results to .csv file. e.g. test_downsample_20160330.csv
    '''

    #
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.datetime.now().strftime("%H:%M:%S")

    #save following result in .csv file, b:bilinear; j:jsvm
    result_file = open(out_result_path + 'test_downsample_%s.csv' %date_now, 'w')
    result_file.write('filename,frames,src_resolution,dst_resolution,'
                      'encode_time_jsvm,fps_jsvm,downsample_time_jsvm,bitstream_size_jsvm,'
                      'psnr_y_jsvm,psnr_u_jsvm,psnr_v_jsvm,')
    result_file.write('encode_time_bilinear,fps_bilinear,downsample_time_bilinear,bitstream_size_bilinear,'
                      'psnr_y_bilinear,psnr_u_bilinear,psnr_v_bilinear,')
    result_file.write('encode_time_tapfilter,fps_tapfilter,downsample_time_tapfilter,bitstream_size_tapfilter,'
                      'psnr_y_tapfilter,psnr_u_tapfilter,psnr_v_tapfilter,\n')

    all_src_sequences = [test_seq_path + 'Mac_Camera_0x106B_Back_Light_Terrible_Head_Shoulder_1280x720_30FPS_I420.yuv',
                         test_seq_path + 'Mac_Camera_0x106B_Move_One_1280x720_30FPS_I420.yuv',
                         test_seq_path + 'iphone5A1429_walking_720x1280.yuv']
    all_down_scale = [2, 4, 8]
    all_downsample_type = ['jsvm', 'bilinear', 'tap-filter']


    for down_scale in all_down_scale:
        for src_sequence in all_src_sequences:
            src_width, src_height, frame_rate = tools_common.get_resolution_from_file_name(src_sequence)
            dst_width = src_width / down_scale
            dst_height = src_height / down_scale

            file_name = os.path.basename(src_sequence)

            #files for jsvm
            sample_file_jsvm = out_result_path + file_name[0:-4] + '_to_%sx%s' %(dst_width, dst_height) + '_jsvm.yuv'
            bitstream_jsvm = sample_file_jsvm[0:-4] + '.264'
            rec_yuv_jsvm = sample_file_jsvm[0:-4] + '_rec.yuv'

            #files for dyadic bilinear down-sampler
            sample_file_bilinear = out_result_path + file_name[0:-4] + '_to_%sx%s' %(dst_width, dst_height) + \
                                   '_bilinear.yuv'
            bitstream_bilinear = sample_file_bilinear[0:-4] + '.264'
            rec_yuv_bilinear = sample_file_bilinear[0:-4] + '_rec.yuv'

            #files for tap-filter down-sampler
            sample_file_tapfilter = out_result_path + file_name[0:-4] + '_to_%sx%s' %(dst_width, dst_height) + \
                                   '_tapfilter.yuv'
            bitstream_tapfilter = sample_file_tapfilter[0:-4] + '.264'
            rec_yuv_tapfilter = sample_file_tapfilter[0:-4] + '_rec.yuv'

            #step 1: down sample files
            total_time_j, frame_time_j = tools_downsampler.jsvm_down_convert(
                src_width, src_height, src_sequence, dst_width, dst_height, sample_file_jsvm)
            total_time_b, frame_time_b = tools_downsampler.wels_downsampler(
                src_width, src_height, src_sequence, dst_width, dst_height, sample_file_bilinear, 0)
            total_time_t, total_time_t = tools_downsampler.wels_downsampler(
                src_width, src_height, src_sequence, dst_width, dst_height, sample_file_tapfilter, 4)

            #step2: encode
            frames_j, encoder_time_j, fps_j, downtime_j = tools_codec.wels_h264_encoder(
                sample_file_jsvm, bitstream_jsvm, dst_width, dst_height, dst_width, dst_height)
            frames_b, encoder_time_b, fps_b, downtime_b = tools_codec.wels_h264_encoder(
                sample_file_bilinear, bitstream_bilinear, dst_width, dst_height, dst_width, dst_height)
            frames_t, encoder_time_t, fps_t, downtime_t = tools_codec.wels_h264_encoder(
                sample_file_tapfilter, bitstream_tapfilter, dst_width, dst_height, dst_width, dst_height)

            bitstream_size_j = os.path.getsize(bitstream_jsvm)
            bitstream_size_b = os.path.getsize(bitstream_bilinear)
            bitstream_size_t = os.path.getsize(bitstream_tapfilter)

            #step3: decode
            tools_codec.wels_h264_decoder(bitstream_jsvm, rec_yuv_jsvm)
            tools_codec.wels_h264_decoder(bitstream_bilinear, rec_yuv_bilinear)
            tools_codec.wels_h264_decoder(bitstream_tapfilter, rec_yuv_tapfilter)

            #step4: calculate psnr
            framenum_j, framerate_j, psnry_j, psnru_j, psnrv_j = tools_common.calculate_PSNR_staticd(
                dst_width, dst_height, sample_file_jsvm, rec_yuv_jsvm)
            framenum_b, framerate_b, psnry_b, psnru_b, psnrv_b = tools_common.calculate_PSNR_staticd(
                dst_width, dst_height, sample_file_bilinear, rec_yuv_bilinear)
            framenum_t, framerate_t, psnry_t, psnru_t, psnrv_t = tools_common.calculate_PSNR_staticd(
                dst_width, dst_height, sample_file_tapfilter, rec_yuv_tapfilter)

            #save results in .csv
            result_file.write('%s,%d,%dx%d,%dx%d,'
                              '%f,%f,%f,%d,'
                              '%f,%f,%f,'
                              %(file_name, frames_j, src_width, src_height, dst_width, dst_height,
                                encoder_time_j, fps_j, total_time_j, bitstream_size_j,
                                psnry_j, psnru_j, psnrv_j))
            result_file.write('%f,%f,%f,%d,'
                              '%f,%f,%f,'
                              %(encoder_time_b, fps_b, total_time_b, bitstream_size_b,
                                psnry_b, psnru_b, psnrv_b))
            result_file.write('%f,%f,%f,%d,'
                              '%f,%f,%f,\n'
                              %(encoder_time_t, fps_t, total_time_t, bitstream_size_t,
                                psnry_t, psnru_t, psnrv_t))
            pass#end of for all_src_sequences
        pass #end of for all_down_scale
    pass #end


if __name__ == '__main__':
    test_sequence_path = '/Users/guangwwa/WorkSpace/test_sequences/SeqCapture/'
    out_file_path = config.OUT_DATA_PATH

    #compare_bilinear_jsvm(test_sequence_path, out_file_path)

    #Mar. 30, 2016
    test_downsampler(test_sequence_path, out_file_path)