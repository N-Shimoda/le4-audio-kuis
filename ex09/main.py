# convert .wav file into volume figure

# 【補足】
# 配列（リスト）のデータ参照
# list[A:B] listのA番目からB-1番目までのデータを取得

# 【補足】
# 配列（リスト）のデータ参照
# list[:B] listの先頭からB-1番目までのデータを取得

import matplotlib.pyplot as plt
import numpy as np
import librosa

# choose from ["catena", "separato"]
data_type = "catena"
print("data type:", data_type)

# サンプリングレート
SR = 16000

# 音声ファイルの読み込み
x, _ = librosa.load('/Users/naoki/github/le4-audio-kuis-main/ex01/' + data_type + '.wav', sr=SR)

#
# 短時間フーリエ変換
#

# create hamming window
size_frame = 512			# 2のべき乗
hamming_window = np.hamming(size_frame)

# シフトサイズ
size_shift = 16000 / 100	# 0.01 sec (10 msec) because 1 sec has size of 16000

# スペクトログラムを保存するlist
volume_data = []
speaking_area = []

# size_shift分ずらしながらsize_frame分のデータを取得
# np.arange関数はfor文で辿りたい数値のリストを返す
# 通常のrange関数と違うのは3つ目の引数で間隔を指定できるところ
# (初期位置, 終了位置, 1ステップで進める間隔)
for i in np.arange(0, len(x)-size_frame, size_shift):
  
  # 該当フレームのデータを取得
  idx = int(i)	# arangeのインデクスはfloatなのでintに変換
  x_frame = x[idx : idx+size_frame]
  
  # calculate RMS
  abs_fft_spec = np.abs( np.fft.rfft(x_frame * hamming_window) )
  rms = np.sqrt(np.sum(abs_fft_spec ** 2) / size_frame)

  # convert RMS into volume [dB]
  volume_dB = 20 * np.log10(rms)

  if volume_dB > -7:
    speaking_area.append(i / SR)

	# 低周波の部分のみを拡大したい場合
	# 例えば、500Hzまでを拡大する
	# また、最後のほうの画像描画処理において、
	# 	extent=[0, len(x), 0, 500], 
	# にする必要があることに注意
	# size_target = int(len(fft_log_abs_spec) * (500 / (SR/2)))
	# fft_log_abs_spec = fft_log_abs_spec[:size_target]

	# 計算した対数振幅スペクトログラムを配列に保存
  volume_data.append(volume_dB)


# Show speaking_area
print("speaking_area is", [speaking_area[0], speaking_area[-1]])
print(volume_data)

#
# スペクトログラムを画像に表示・保存
#

fig = plt.figure()
x_data = np.arange(0, len(volume_data)*size_shift/SR, size_shift/SR)

# スペクトログラムを描画
plt.xlabel('time [s]')		# x軸のラベルを設定
plt.ylabel('Volume [dB]')				# y軸のラベルを設定
plt.plot(x_data, volume_data)			# 描画

# 表示
plt.show()

# 画像ファイルに保存
fig.savefig('fig/volume_' + data_type + '.png')