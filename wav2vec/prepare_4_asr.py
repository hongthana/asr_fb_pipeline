"""
Command : prepare_data.py --src [...] --dst [...]
"""
import argparse
import os
import sox

from tqdm import tqdm
extension = ".h5context"


def findaudiofiles(dir):
    files = []
    for dirpath, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".wav"):
                files.append(os.path.join(dirpath, filename))
    return files



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aishell Dataset creation.")
    parser.add_argument("--src", default="/home/psc/Desktop/code/asr/data/aishell_v1/data_aishell", help="source directory")
    parser.add_argument("--dst", help="destination directory", default="./")
    args = parser.parse_args()

    transcript_subpath = os.path.join(args.src, "transcript/aishell_transcript_v0.8.txt")
    transcripts_dict = {}
    with open(transcript_subpath, 'r', encoding="utf-8") as f:
        for line in f:
            fname, transcript = line.split(None, 1)
            transcripts_dict[fname] = transcript.strip()

    subpaths = ["wav2vec/train", "wav2vec/dev", "wav2vec/test"]
    for subpath in subpaths:
        src = os.path.join(args.src, subpath)
        dst = os.path.join(args.dst, os.path.basename(subpath) + ".lst")

        with open(dst, "w") as f:
            for cur_f in os.listdir(src):
                if cur_f.lower().endswith(extension):
                    audio_name = cur_f.replace(extension, "")
                    audio_path = os.path.join(src, cur_f)
                    audio_len = "5"  # str(sox.file_info.duration(audio_path))

                    cur_transcript = transcripts_dict.get(audio_name, "")
                    if "" == cur_transcript:
                        print(audio_name)
                        os.system("rm %s" % audio_path)
                        continue

                    writeline = []
                    writeline.append(audio_name)
                    writeline.append(audio_path)
                    writeline.append(audio_len)
                    writeline.append(cur_transcript)
                    f.write("\t".join(writeline) + "\n")




