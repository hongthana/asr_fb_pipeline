import torch
from fairseq.models.wav2vec import Wav2VecModel

# ---------------wav2vec demo-------------------------
# cp = torch.load('../resources/wav2vec_large.pt', map_location=torch.device('cpu'))
# model = Wav2VecModel.build_model(cp['args'], task=None)
# model.load_state_dict(cp['model'])
# model.eval()
#
# wav_input_16khz = torch.randn(1, 10000)
# z = model.feature_extractor(wav_input_16khz)
# c = model.feature_aggregator(z)
# print(z.shape)   # ([1, 512, 60])
# print(c.shape)   # ([1, 512, 60]),


# ------------------vq-wav2vec demo-----------------------
cp = torch.load('../resources/vq-wav2vec_kmeans.pt', map_location=torch.device('cpu'))    # vq-wav2vec_kmeans.pt    vq-wav2vec.pt
model = Wav2VecModel.build_model(cp['args'], task=None)
model.load_state_dict(cp['model'])
model.eval()

wav_input_16khz = torch.randn(1, 10000)
z = model.feature_extractor(wav_input_16khz)
tt, idxs = model.vector_quantizer.forward_idx(z)
print(z.shape)     # ([1, 512, 60])
print(idxs.shape)  # output: torch.Size([1, 60, 2]), 60 timesteps with 2 indexes corresponding to 2 groups in the model