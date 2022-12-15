import librosa
import numpy as np
from src.melody_funs import estimate_melody_f0


def process_data(filename):

  size_frame = 4096	# フレームサイズ
  SR = 16000			# サンプリングレート
  size_shift = 16000 / 100	# シフトサイズ = 0.001 秒 (10 msec)

  # 音声ファイルを読み込む
  x, _ = librosa.load(filename, sr=SR)

  # ファイルサイズ（秒）
  duration = len(x) / SR

  # ハミング窓
  hamming_window = np.hamming(size_frame)

  # スペクトログラムを保存するlist
  spectrogram = []
  melody = []

  # フレーム毎にスペクトルを計算
  for i in np.arange(0, len(x)-size_frame, size_shift):
    # 該当フレームのデータを取得
    idx = int(i)	# arangeのインデクスはfloatなのでintに変換
    x_frame = x[idx : idx+size_frame]
    
    # スペクトル
    fft_spec = np.fft.rfft(x_frame * hamming_window)
    fft_log_abs_spec = np.log(np.abs(fft_spec))
    spectrogram.append(fft_log_abs_spec)
    
    # Estimate frequency of melody
    nn_range = np.arange(36,61,0.1)   # range of note number
    _, melody_f0 = estimate_melody_f0(nn_range, fft_log_abs_spec, SR)
    melody.append(melody_f0)

  preference = [SR, size_frame, size_shift, duration]

  return spectrogram, melody, preference