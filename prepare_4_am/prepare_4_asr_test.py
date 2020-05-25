from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import sys
import re
import sox
# from zhon.hanzi import punctuation   # pip install zhon

punc = "＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､　、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。"

def filterPunctuation(x):
    x = re.sub(r"[%s]+" % punc, "", x)
    return x


def findtranscriptfiles(dir):
    files = []
    for dirpath, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".txt"):
                files.append(os.path.join(dirpath, filename))
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset process for test.")
    parser.add_argument("--base_dir", default='/home/psc/Desktop/code/asr/data/test', help="source directory")
    parser.add_argument("--dst", default='output', help="destination directory")
    args = parser.parse_args()

    wav_dir = os.path.join(args.base_dir, "wav")
    assert os.path.isdir(str(wav_dir)), "wav_dir directory not found - '{d}'".format(d=wav_dir)

    os.makedirs(args.dst, exist_ok=True)
    lists_dst = os.path.join(args.dst, "lists")
    os.makedirs(lists_dst, exist_ok=True)

    transcriptfile_list = findtranscriptfiles(args.base_dir)
    transcripts_dict = {}
    for transcriptfile in transcriptfile_list:
        with open(transcriptfile, "r") as fr:
            for line in fr:
                fname, transcript = line.split("<--->", 1)
                transcripts_dict[fname] = filterPunctuation(transcript.strip())

    subpaths = ["xinwen"]
    for subpath in subpaths:
        cur_wav_dir = os.path.join(wav_dir, subpath)

        assert os.path.exists(cur_wav_dir), "Unable to find the directory - '{src}'".format(src=cur_wav_dir)
        dst = os.path.join(lists_dst, subpath + ".lst")
        sys.stdout.write("analyzing {src}...\n".format(src=cur_wav_dir))
        sys.stdout.flush()

        with open(dst, "w") as f:
            for dirpath, _, filenames in os.walk(cur_wav_dir):
                for filename in filenames:
                    if filename.endswith(".wav"):
                        wav_filename = filename.replace(".wav", "")
                        audio_path = os.path.join(dirpath, filename)
                        handle = os.path.basename(dirpath)
                        if not os.path.exists(audio_path):
                            # print("'{src}' cannot find vec file".format(src=filename))
                            continue

                        cur_trans = transcripts_dict.get(wav_filename, "")
                        if "" == cur_trans:
                            print(wav_filename, " have not transtext")
                            continue

                        cur_trans_new = ""
                        length = len(cur_trans)
                        i = 0
                        while i < length - 1:
                            cur_trans_new += cur_trans[i] + " "
                            i += 1
                        cur_trans_new += cur_trans[length - 1]

                        writeline = []
                        writeline.append(subpath + "-" + handle)  # sampleid
                        writeline.append(audio_path)
                        writeline.append(str(sox.file_info.duration(audio_path)))  # length
                        writeline.append(cur_trans_new)
                        f.write("\t".join(writeline) + "\n")
