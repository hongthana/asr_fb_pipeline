# -*- coding: UTF-8 -*-
import sox
import os
import glob


def check_audio_len_and_16k(folder_in):
    for wav_id in os.listdir(folder_in):
        cur_audio_path = os.path.join(folder_in, wav_id)
        audio_len = sox.file_info.duration(cur_audio_path)
        if audio_len > 9.9 and audio_len < 30.1:
            continue
        else:
            os.remove(cur_audio_path)


ext = "mp4"

dir_path = "/home/psc/Desktop/code/asr/data/cctv_data"
dst_path = dir_path + "_processed"
search_path = os.path.join(dir_path, '**/*.' + ext)
os.makedirs(dst_path, exist_ok=True)

for fname in glob.iglob(search_path, recursive=True):
    audio_path = os.path.realpath(fname)
    base_dir_name = os.path.basename(os.path.dirname(fname))
    save_dir = os.path.join(dst_path, base_dir_name)
    os.makedirs(save_dir, exist_ok=True)
    audio_save_path = os.path.join(save_dir, os.path.basename(fname).replace(".mp4", ".wav"))
    print("cur process: {}".format(audio_path))

    os.system("ffmpeg -i {} -hide_banner -loglevel 0 -ac 1 -ar 16000 {}".format(audio_path, audio_save_path))

    cur_split_dir = os.path.join(save_dir, os.path.basename(fname).replace(".mp4", ""))
    os.makedirs(cur_split_dir, exist_ok=True)
    os.system("python3 ../audiosplit.py --target_dir {} --output_dir {}".format(audio_save_path, cur_split_dir))
    os.remove(audio_save_path)
    os.system("python3 ../audiosplit.py --target_dir {} --output_dir {}".format(cur_split_dir, cur_split_dir))

    check_audio_len_and_16k(cur_split_dir)

