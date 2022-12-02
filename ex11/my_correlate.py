#
# 計算機科学実験及演習 4「音響信号処理」
# サンプルソースコード
#
# 音声ファイルを読み込み，フーリエ変換を行う．
#

# ライブラリの読み込み
import matplotlib.pyplot as plt
import numpy as np
import librosa


# 配列 a の index 番目の要素がピーク（両隣よりも大きい）であれば True を返す
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


# サンプリングレート
SR = 16000

# choose from ["catena", "separato"]
data_type = "separato"
print("data type: [", data_type, "]")

# load .wav file
x, _ = librosa.load('/Users/naoki/github/le4-audio-kuis-main/ex01/' + data_type + '.wav', sr=SR)

# フレームサイズ, 窓関数, シフト幅
size_frame = 512			# 2のべき乗
hamming_window = np.hamming(size_frame)
size_shift = 16000 / 100	# 0.01 秒 (10 msec)

# 基底周波数 f0 を保存するlist
f0_list = []

# Extract data by hamming_window and calculate f0 for each frames.
for i in np.arange(0, len(x)-size_frame, size_shift):

  # 該当フレームのデータを取得
  idx = int(i)	# arangeのインデクスはfloatなのでintに変換
  x_frame = x[idx : idx+size_frame]
  
  f0 = calculate_f0(x_frame, SR)
  f0_list.append(f0)

# create figure
fig = plt.figure()
plt.xlabel('Time [s]')
plt.ylabel('f0 [Hz]')
plt.plot(f0_list)
plt.show()

fig.savefig('ex11/fig/f0_' + data_type + '.png')