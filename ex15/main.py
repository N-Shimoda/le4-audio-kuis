# see also `src/zerocross.py`

"""
import sys
sys.path.append("../")
# from src.zero_cross import zero_cross_short
import src.zero_cross as zero_cross
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt
import zero_cross

# same code as ex11/my_correlate.py
def is_peak(a, index):

  # （自分で実装すること，passは消す）
  # 2 abnormal cases 
  if index == 0:
    result = (a[index] < a[index+1])
  elif index == len(a)-1:
    result = a[index-1] < a[index]

  else:
    result = a[index-1] < a[index] and a[index] < a[index+1]

  return result


# same code as ex11/my_correlate.py
def calculate_f0(x_frame, SR):

  # 自己相関が格納された，長さが len(x)*2-1 の対称な配列を得る
  autocorr = np.correlate(x_frame, x_frame, 'full')

  # この autocorr の値は対称になっているため、不要な前半を捨てる
  autocorr = autocorr [len(autocorr) // 2 : ]
  # print("size of autocorr", len(autocorr))

  # ピークのインデックス(τ)を抽出する．この時点では「極大値」を含む
  peakindices = [i for i in range (len (autocorr )) if is_peak (autocorr, i)]

  # インデックス0 がピークに含まれていれば捨てる
  peakindices = [i for i in peakindices if i != 0]

  # print(peakindices)
  # print("size of peakindices", len(peakindices))

  # 自己相関が最大となるインデックスを得る
  max_peak_index = max(peakindices , key=lambda index: autocorr[index])
  # print(max_peak_index)

  # インデックスに対応する周波数を得る
  # （自分で実装すること）
  tau = max_peak_index / SR
  f0 = 1 / tau  # because τ = 1/f0
  # print("f0:", f0, "Hz")

  return f0


"""
  Function to judge if a sound frame is voiced
  params : sound_frame
           f0   [fundamental frequency]
  return : True or False
"""
def isVoiceSound(sound_frame, f0):

  # calculate zero cross
  zc = zero_cross.zero_cross_short(sound_frame)

  # acceptable error
  alpha = 100

  # return ( f0*(2-alpha) < zc and zc < f0*(2+alpha) )
  return True


# Sampling Rate
SR = 16000

# load sound file (.wav)
x, _ = librosa.load('/Users/naoki/github/le4-audio-kuis-main/ex15/sound.wav', sr=SR)

# フレームサイズ, 窓関数, シフトサイズ
size_frame = 512          # 2のべき乗
hamming_window = np.hamming(size_frame)
size_shift = 16000 / 100	# 0.01 秒 (10 msec)

# fundamental frequency
f0_list = []
spectrogram = []

# 元データをフレームごとに分割
for i in np.arange(0, len(x)-size_frame, size_shift):
  
  # 該当フレームのデータを取得
  idx = int(i)	# arangeのインデクスはfloatなのでintに変換
  x_frame = x[idx : idx+size_frame]
  
  # calculate f0
  f0 = calculate_f0(x_frame, SR)

  # if x_frame is not voice sound, f0 should be 0
  if( isVoiceSound(x_frame, f0) ):
    f0_list.append(f0)
  else:
    f0_list.append(0)

  
  fft_spec = np.fft.rfft(x_frame * hamming_window)
  fft_log_abs_spec = np.log(np.abs(fft_spec))
  spectrogram.append(fft_log_abs_spec)


# Create Figure of spectrogram & f0
fig = plt.figure()

# draw spectrogram
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Frequency [Hz]')
ax1.imshow(
  np.flipud(np.array(spectrogram).T),
  extent=[0, len(x)/SR, 0, 8000],     # 2nd arg is `duration` (i.e. filesize)
  aspect='auto',
  interpolation='nearest'
)

# draw f0
ax2 = ax1.twinx()
ax2.set_ylabel('frequency of f0 [Hz]')
x_data = np.linspace(0, len(x)/SR, len(f0_list))
ax2.plot(x_data, f0_list, c='y')

plt.show()

fig.savefig("ex15/fig/spectrogram_with_f0.png")