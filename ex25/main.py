import math
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt
import librosa

"""
  正弦波を生成する関数
  params : sampling_rate ... サンプリングレート
           frequency ... 生成する正弦波の周波数
           duration ... 生成する正弦波の時間的長さ
  return : 2πft
"""
def generate_sinusoid(sampling_rate, frequency, duration):
	sampling_interval = 1.0 / sampling_rate
	t = np.arange(sampling_rate * duration) * sampling_interval
	waveform = np.sin(2.0 * math.pi * frequency * t)
	return waveform


SR = 16000
x, _ = librosa.load('ex02/a.wav', sr=SR)

# 生成する正弦波の周波数（Hz）
D = 2.0
R = 100
f_s = 300
frequency = R/f_s

# 生成する正弦波の時間的長さ
duration = len(x)

# 正弦波を生成する
sin_wave = generate_sinusoid(SR, frequency, duration/SR)

# 最大値を0.9にする
sin_wave = sin_wave * 0.9

# 元の音声と正弦波を重ね合わせる
x_changed = x * (1 + D*sin_wave)

# 値の範囲を[-1.0 ~ +1.0] から [-32768 ~ +32767] へ変換する
x_changed = (x_changed * 32768.0). astype('int16')

# 音声ファイルとして出力する
filename = 'ex25/out/voice_change_freq={}.wav'.format(frequency)
scipy.io.wavfile.write(filename , int(SR), x_changed)


#
# Calculate spectrum of 'x_changed'
fft_spec = np.fft.rfft(x_changed)
fft_log_abs_spec = np.log(np.abs(fft_spec))


#
# Draw spectrum of 'x_changed'
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.set_xlabel('sec')
ax1.set_ylabel('amplitude')
ax1.set_xlim([0, SR/2])

x_data = np.fft.rfftfreq(len(x_changed), d=1/SR)
ax1.plot(x_data, fft_log_abs_spec)

plt.show()
fig.savefig('ex25/out/result_freq={}.png'.format(frequency))