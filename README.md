Pipeline:

Audios -> Feature extraction (Wav2Vec) -> Acoustic Modeling (wav2letter) -> Language Model (LM) -> Decoding --> Texts

Audios:
	
	cctv的youtube地址：https://www.youtube.com/channel/UCcLK3j-XWdGBnt5bR9NJHaQ，
	目前下载了新闻联播, 焦点访谈, 面对面三个栏目的mp4 720的视频，然后转换成16k的wav格式，并使用py-webrtcvad进行分割。处理脚本 data/cctv_preprocess.py
	aishell v1 + v2的音频，只取时长位于10秒～30秒的音频。






相关repos:

	https://github.com/luweishuang/process_audios.git
