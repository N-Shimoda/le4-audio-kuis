import librosa
import numpy as np
import pickle
from src.melody_funs import estimate_melody_f0
from src.speech_model import recognize_word


"""
  Function to analyze sound, and return values that reflects features.
  params : filename of .wav file
  return : spectrogram, melody, speech, preference
"""
def analyze_sound(filename):

  # 
  # Load parameters of speech recognition
  with open("ex16/mu_sigma_result.pickle", mode="rb") as f:

    mu_sigma_result = pickle.load(f)

    # preference of frame
    dim = mu_sigma_result[4][0]
    size_frame = mu_sigma_result[4][1]
    size_shift = mu_sigma_result[4][2]

  
  # preference of frame
  # size_frame = 4096	# フレームサイズ
  SR = 16000			# サンプリングレート
  # size_shift = 16000 / 100	# シフトサイズ = 0.001 秒 (10 msec)
  hamming_window = np.hamming(size_frame)   # ハミング窓

  # 音声ファイルを読み込む
  x, _ = librosa.load(filename, sr=SR)

  # ファイルサイズ（秒）
  duration = len(x) / SR

  # lists for storing result
  spectrogram = []
  melody = []
  speech = []
  preference = [SR, size_frame, size_shift, duration]


  # divide data into frames
  for i in np.arange(0, len(x)-size_frame, size_shift):
    # 該当フレームのデータを取得
    idx = int(i)	# arangeのインデクスはfloatなのでintに変換
    x_frame = x[idx : idx+size_frame]
    
    #
    # Spectrum
    fft_spec = np.fft.rfft(x_frame * hamming_window)
    fft_log_abs_spec = np.log(np.abs(fft_spec))
    spectrogram.append(fft_log_abs_spec)
    
    #
    # Estimate frequency of melody
    nn_range = np.arange(36,61,0.1)   # range of note number
    _, melody_f0 = estimate_melody_f0(nn_range, fft_log_abs_spec, SR)
    melody.append(melody_f0)

    #
    # Speech recognition
    # Calculate cepstrum
    amp_spectrum = np.fft.rfft(x_frame)
    log_abs_spectrum = np.log( np.abs(amp_spectrum) )
    cepstrum = np.abs( np.fft.fft(log_abs_spectrum) )

    # extract cepstrum of low index (0~dim & -dim~)
    # cepstrum = np.concatenate([cepstrum[:dim], cepstrum[-dim:]])
    cepstrum = cepstrum[:dim]

    speech.append( recognize_word(cepstrum) )

  return spectrogram, melody, speech, preference