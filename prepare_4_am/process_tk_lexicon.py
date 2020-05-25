from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import sys
import sox


if __name__ == "__main__":
    base_dir = "/home/psc/Desktop/code/asr/asr_fb_pipeline/prepare_4_am/data"

    src_token_file = os.path.join(base_dir, "am/tokens.txt")
    dst_lexicon_file = os.path.join(os.path.dirname(src_token_file), "lexicon_new.txt")
    # all_chars = []
    # with open(src_token_file, "r") as fr:
    #     for line in fr:
    #         cur_char = line.strip()
    #         all_chars.append(cur_char)
    #
    # with open(dst_lexicon_file, "w", encoding="utf-8") as f:
    #     for w in list(set(all_chars)):
    #         f.write(w)
    #         f.write("\t")
    #         f.write(w)
    #         f.write(" \n")

    subpaths = ["train", "dev", "test"]
    lists_dir = os.path.join(base_dir, "vec_lists")
    for subpath in subpaths:
        cur_list_file = os.path.join(lists_dir, subpath+".lst")
        dst_list_file = os.path.join(lists_dir, subpath + "_new.lst")
        with open(cur_list_file, "r") as fr, open(dst_list_file, "w") as fw:
            for line in fr:
                sampleid, file_path, file_len, file_trans = line.strip().split("\t")
                cur_trans = file_trans.replace(" ", "")
                # file_trans_new = " ".join(cur_trans.split(None))
                file_trans_new = ""
                length = len(cur_trans)
                i = 0
                while i < length-1:
                    file_trans_new += cur_trans[i] + " "
                    i += 1
                file_trans_new += cur_trans[length-1]

                writeline = []
                writeline.append(sampleid)
                writeline.append(file_path)
                writeline.append(file_len)
                writeline.append(file_trans_new)
                fw.write("\t".join(writeline) + "\n")





