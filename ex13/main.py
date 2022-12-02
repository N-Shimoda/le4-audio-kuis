#
# 計算機科学実験及演習 4「音響信号処理」
# サンプルソースコード
#
# ケプストラムを計算する関数
#

# see also `src/plot_spectrum.py`, `src/cepstrum.py`

import numpy as np
import matplotlib.pyplot as plt
import librosa


# スペクトルを受け取り，ケプストラムを返す関数
def get_cepstrum(amplitude_spectrum):

	log_spectrum = np.log(amplitude_spectrum)
	cepstrum = np.fft.fft(log_spectrum)

	return cepstrum


# サンプリングレート
SR = 16000

# choose from ["catena", "separato"]
data_type = "catena"
print("data type: [", data_type, "]")

# load sound file (.wav)
x, _ = librosa.load('/Users/naoki/github/le4-audio-kuis-main/ex01/' + data_type + '.wav', sr=SR)


# Step1,2: 振幅スペクトルの対数をとる
# fft_spec = np.fft.rfft(x)
amplitude_spectrum = np.fft.rfft(x)
cepstrum = get_cepstrum(np.abs(amplitude_spectrum))

fft_log_abs_spec = np.log(np.abs(amplitude_spectrum))

print("length of cepstrum:", len(cepstrum))

# Step3: Get cepstrum of the 13 lowest frequency
cepstrum[14:] = 0

# Step4: apply inverse-FFT
spectrum_envelope = np.fft.ifft(cepstrum)

"""
# (複素スペクトルを対数振幅スペクトルに)
fft_log_abs_spec = np.log(np.abs(fft_spec))
"""

# save figure
fig = plt.figure()
plt.xlabel('frequency [Hz]')
plt.ylabel('amplitude')
plt.plot(fft_log_abs_spec)
plt.plot(spectrum_envelope)
plt.show()

# 画像ファイルに保存
fig.savefig('ex13/fig/plot-spectrum-whole.png')

"""
# 横軸を0~2000Hzに拡大
# xlimで表示の領域を変えるだけ
fig = plt.figure()
plt.xlabel('frequency [Hz]')
plt.ylabel('amplitude')
plt.xlim([0, 2000])
plt.plot(x_data, fft_log_abs_spec)

# 表示
plt.show()

# 画像ファイルに保存
fig.savefig('img/plot-spectrum-2000.png')
"""