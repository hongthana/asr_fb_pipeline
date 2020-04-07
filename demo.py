from stt import Transcriber
import os

transcriber = Transcriber(w2letter = '../wav2letter',
                          w2vec = 'resources/wav2vec_self.pt',
                          am = 'resources/am.bin',
                          tokens = 'resources/tokens.txt',
                          lexicon = 'resources/lexicon.txt',
                          lm = 'resources/lm.bin',
                          temp_path = './temp',
                          nthread_decoder = 4)

transcriber.transcribe(['data/tets1.wav'])

# wav_list = []
# base_dir = '/home/psc/Desktop/code/asr/data/vivos/test/waves'
# for sub_dir in os.listdir(base_dir):
#     sub_dir_abs = os.path.join(base_dir, sub_dir)
#     for cur_file in os.listdir(sub_dir_abs):
#         wav_file = os.path.join(sub_dir_abs, cur_file)
#         if os.path.exists(wav_file) and wav_file.lower().endswith("wav"):
#             wav_list.append(wav_file)
#
# print("all number in wav_list = %d " % len(wav_list))
# transcriber.transcribe(wav_list)

