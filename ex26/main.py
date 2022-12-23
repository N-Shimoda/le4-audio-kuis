import math
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt
import librosa

"""
  正弦波を生成する関数
  params : sampling_rate ... サンプリングレート
           frequency (f) ... 生成する正弦波の周波数
           duration ... 生成する正弦波の時間的長さ
  return : 2πft
"""
def generate_sinusoid(sampling_rate, frequency, duration):
	sampling_interval = 1.0 / sampling_rate
	t = np.arange(sampling_rate * duration) * sampling_interval
	waveform = np.sin(2.0 * math.pi * frequency * t)
	return waveform


SR = 16000
name = 'kimigayo'
x, _ = librosa.load('sound/kimigayo_trim.wav', sr=SR)

# 
D = 1
R = SR * 10
f_s = SR
frequency = R/f_s

# 生成する正弦波の時間的長さ
duration = len(x)

# vibrato
tau_0 = 10
tau = (tau_0 + D/SR * generate_sinusoid(SR, frequency, duration/SR))
x_changed = np.roll(x, -tau)

# 値の範囲を[-1.0 ~ +1.0] から [-32768 ~ +32767] へ変換する
x_changed = (x_changed * 32768.0). astype('int16')

# 音声ファイルとして出力する
filename = 'ex25/out/{}/wav/changed_freq={}_D={}.wav'.format(name, frequency, D)
scipy.io.wavfile.write(filename , int(SR), x_changed)


#
# Calculate and draw spectrum of 'x_changed'
fft_spec = np.fft.rfft(x_changed)
fft_log_abs_spec = np.log(np.abs(fft_spec))

# Figure
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.set_xlabel('sec')
ax1.set_ylabel('amplitude')
ax1.set_xlim([0, SR/2])

x_data = np.fft.rfftfreq(len(x_changed), d=1/SR)
ax1.plot(x_data, fft_log_abs_spec)

plt.show()
fig.savefig('ex25/out/{}/fig/spectrum_freq={}_D={}.png'.format(name, frequency, D))