import librosa
import numpy as np
import scipy.io.wavfile
import math
import os


def apply_effect(filename, effect_select):

  x_changed = None
  
  out_dir = "kadai2/effect-middle"
  basename = os.path.basename(filename)
  SR = 16000

  effect_list = [
    ["Tremolo", _apply_tremolo],
    ["Voice Change", _apply_voice_change],
    ["Vibrato", _apply_vibrato]
  ]

  for effect in effect_list:
    if effect[0] == effect_select:
      x_changed = effect[1](filename)

  if x_changed is None:
    raise ValueError("No match in apply_effect")

  # 音声ファイルとして出力する
  out_path = out_dir + "/" + basename
  scipy.io.wavfile.write(out_path, int(SR), x_changed)
  return out_path


def _apply_voice_change(filename):

  SR = 16000
  x, _ = librosa.load(filename, sr=SR)

  # 生成する正弦波の周波数（Hz）
  frequency = 300

  # 生成する正弦波の時間的長さ
  duration = len(x)

  # 正弦波を生成する
  sin_wave = _generate_sinusoid(SR, frequency, duration/SR)

  # 最大値を0.9にする
  sin_wave = sin_wave * 0.9

  # 元の音声と正弦波を重ね合わせる
  x_changed = x * sin_wave

  # Calculate spectrum of 'x_changed'
  fft_spec = np.fft.rfft(x_changed)
  fft_log_abs_spec = np.log(np.abs(fft_spec))

  # 値の範囲を[-1.0 ~ +1.0] から [-32768 ~ +32767] へ変換する
  # 16bitで表される数の範囲 (2^15)
  x_changed = (x_changed * 32768.0). astype('int16')

  return x_changed


def _apply_tremolo(filename):

  SR = 16000
  x, _ = librosa.load(filename, sr=SR)

  # 
  D = 1
  R = SR * 10
  f_s = SR
  frequency = R/f_s

  # 生成する正弦波の時間的長さ
  duration = len(x)

  # 正弦波を生成する
  A = 1 + D * _generate_sinusoid(SR, frequency, duration/SR)

  # 元の音声と正弦波を重ね合わせる
  x_changed = x * A

  # 値の範囲を[-1.0 ~ +1.0] から [-32768 ~ +32767] へ変換する
  x_changed = (x_changed * 32768.0). astype('int16')

  return x_changed


"""
  params : filename of sound file (.wav)
  return : x_changed
"""
def _apply_vibrato(filename):

  SR = 16000
  x, _ = librosa.load(filename, sr=SR)

  #
  # Parameters (D,R)
  D = SR * 10   # amplitude of time difference
  R = SR * 5   # frequency of time difference
  frequency = R/SR    # note: f_s = SR

  # 生成する正弦波の時間的長さ
  duration = len(x)

  # vibrato
  tau_0 = 10
  tau = np.int64(tau_0 + D/SR * _generate_sinusoid(SR, frequency, duration/SR))
  x_changed_values = []
  for i in range(len(x)):
    x_changed_values.append(x[i-tau[i]])

  x_changed = np.array(x_changed_values)

  # 値の範囲を[-1.0 ~ +1.0] から [-32768 ~ +32767] へ変換する
  x_changed = (x_changed * 32768.0). astype('int16')

  return x_changed


"""
  正弦波を生成する関数
  params : sampling_rate ... サンプリングレート
           frequency ... 生成する正弦波の周波数
           duration ... 生成する正弦波の時間的長さ
  return : 2πft
"""
def _generate_sinusoid(sampling_rate, frequency, duration):
	sampling_interval = 1.0 / sampling_rate
	t = np.arange(sampling_rate * duration) * sampling_interval
	waveform = np.sin(2.0 * math.pi * frequency * t)
	return waveform