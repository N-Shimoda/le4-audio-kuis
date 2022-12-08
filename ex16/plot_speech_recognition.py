import matplotlib.pyplot as plt
import numpy as np
import librosa
import my_models

dim = 13

# 
# Step1: Load sound file and parameters
#

# load .wav file
SR = 16000
x, _ = librosa.load('ex16/sound/aiueo.wav', sr=SR)


#
# Step2: Use `Short-time Fourie Transform` to
#   (i)  calculate spectrogram 
#   (ii) conduct speech recognition
#

# preference of frame
size_frame = 512			# 2のべき乗
hamming_window = np.hamming(size_frame)
size_shift = SR / 100	# 0.01 秒 (10 msec)

# list for storing results
spectrogram = []
recognition = []


# calculate spectrum & word recognition for each frames
for i in np.arange(0, len(x)-size_frame, size_shift):
  
  # sound data of current frame
  idx = int(i)
  x_frame = x[idx : idx+size_frame]

  #
  # Step2-(i): Calculate spectrum
  fft_spec = np.fft.rfft(x_frame * hamming_window)
  fft_log_abs_spec = np.log(np.abs(fft_spec))
  spectrogram.append(fft_log_abs_spec)

  #
  # Step2-(ii): Speech recognition

  # Calculate cepstrum
  amp_spectrum = np.fft.rfft(x_frame)
  log_abs_spectrum = np.log( np.abs(amp_spectrum) )
  cepstrum = np.fft.fft(log_abs_spectrum)

  # extract cepstrum of low index (0~dim & -dim~)
  cepstrum = np.concatenate([cepstrum[:dim], cepstrum[-dim:]])

  recognition.append( my_models.recognize_word(cepstrum) )


# 
# Draw Figure
#
# preference of figure
fig = plt.figure()

# draw spectrogram
plt.title('Spectrogram with speech recognition')
plt.xlabel('Time [s]')					# x軸のラベルを設定
plt.ylabel('Frequency [Hz]')		# y軸のラベルを設定
plt.imshow(
	np.flipud(np.array(spectrogram).T),		# 画像とみなすために，データを転置して上下反転
	extent=[0, len(x), 0, SR/2],			# (横軸の原点の値，横軸の最大値，縦軸の原点の値，縦軸の最大値)
	aspect='auto',
	interpolation='nearest'
)
plt.show()


# save as .png file
fig.savefig('ex16/fig/spectrogram_with_recognition.png')