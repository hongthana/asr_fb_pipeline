from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import sys
import sox


def findtranscriptfiles(dir):
    files = []
    for dirpath, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".trans.txt"):
                files.append(os.path.join(dirpath, filename))
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Librispeech Dataset creation.")
    parser.add_argument("--base_dir", default='/home/psc/Desktop/code/asr/data/aishell_v1/data_aishell', help="source directory")
    parser.add_argument("--dst", default='output', help="destination directory")
    args = parser.parse_args()

    wav_dir = os.path.join(args.base_dir, "wav")
    vec_dir = os.path.join(args.base_dir, "vec")
    assert os.path.isdir(str(wav_dir)), "aishell wav_dir directory not found - '{d}'".format(d=wav_dir)
    assert os.path.isdir(str(vec_dir)), "aishell vec_dir directory not found - '{d}'".format(d=vec_dir)
    os.makedirs(args.dst, exist_ok=True)
    lists_dst = os.path.join(args.dst, "lists")
    os.makedirs(lists_dst, exist_ok=True)
    am_dst = os.path.join(args.dst, "am")
    os.makedirs(am_dst, exist_ok=True)

    transcriptfile = os.path.join(args.base_dir, "transcript/aishell_transcript_v0.8.txt")
    transcripts_dict = {}
    all_chars = []
    with open(transcriptfile, "r") as fr:
        for line in fr:
            fname, transcript = line.split(None, 1)
            transcripts_dict[fname] = transcript.strip()
            for c in transcript.strip():
                all_chars.append(c)

    train_dev_words = {}
    subpaths = ["train", "dev", "test"]
    for subpath in subpaths:
        cur_wav_dir = os.path.join(wav_dir, subpath)
        cur_vec_dir = os.path.join(vec_dir, subpath)

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
                        vec_path = os.path.join(cur_vec_dir, filename.replace(".wav", ".h5context"))
                        if not os.path.exists(vec_path):
                            # print("'{src}' cannot find vec file".format(src=filename))
                            continue

                        cur_transcript = transcripts_dict.get(wav_filename, "")
                        if "" == cur_transcript:
                            print(wav_filename)
                            continue

                        writeline = []
                        writeline.append(subpath + "-" + handle)  # sampleid
                        writeline.append(vec_path)
                        writeline.append(str(sox.file_info.duration(audio_path)))  # length
                        writeline.append(cur_transcript)
                        f.write("\t".join(writeline) + "\n")

                        if "train" in subpath or "dev" in subpath:
                            for w in cur_transcript.split():
                                train_dev_words[w] = True

    # create tokens dictionary
    tkn_file = os.path.join(am_dst, "tokens.txt")
    sys.stdout.write("creating tokens file {t}...\n".format(t=tkn_file))
    sys.stdout.flush()
    with open(tkn_file, "w") as f:
        f.write("|\n")
        for c in list(set(all_chars)):
            f.write(c + "\n")

    # create leixcon
    lexicon_file = os.path.join(am_dst, "lexicon.txt")
    sys.stdout.write("creating train lexicon file {t}...\n".format(t=tkn_file))
    sys.stdout.flush()
    with open(lexicon_file, "w", encoding="utf-8") as f:
        for w in train_dev_words.keys():
            f.write(w)
            f.write("\t")
            f.write(" ".join(w))
            f.write(" |\n")
    sys.stdout.write("Done !\n")


