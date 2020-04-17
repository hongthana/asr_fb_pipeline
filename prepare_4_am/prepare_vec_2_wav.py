from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Librispeech Dataset creation.")
    parser.add_argument("--base_dir", default='/home/psc/lists', help="source directory")
    args = parser.parse_args()

    wavlist_dir = args.base_dir + "_wav"
    os.makedirs(wavlist_dir, exist_ok=True)

    subpaths = ["train.lst", "dev.lst", "test.lst"]
    for subpath in subpaths:
        cur_veclist_file = os.path.join(args.base_dir, subpath)
        dst_wavlist_path = os.path.join(wavlist_dir, subpath)
        with open(cur_veclist_file, "r") as fr, open(dst_wavlist_path, "w") as fw:
            for line in fr:
                sp_id, vec_path, cur_len, cur_trans = line.strip().split("\t")
                wav_path = vec_path.replace(".h5context", ".wav")
                t1 = os.path.dirname(wav_path)
                t2 = os.path.basename(wav_path)
                new_wav_path = os.path.dirname(wav_path) + '/' + sp_id + '/' + os.path.basename(wav_path)
                if not os.path.exists(new_wav_path):
                    print(new_wav_path, " is not exist")
                    continue
                writeline = []
                writeline.append(sp_id)  # sampleid
                writeline.append(new_wav_path)
                writeline.append(cur_len)  # length
                writeline.append(cur_trans)
                fw.write("\t".join(writeline) + "\n")
