import matplotlib.pyplot as plt
import numpy as np
import librosa
import pickle
import my_models

# 
# Step1: Load parameters and sound file
#

# Parameters
with open("ex16/mu_sigma_result.pickle", mode="rb") as f:

  mu_sigma_result = pickle.load(f)

  # preference of frame
  dim = mu_sigma_result[4][0]
  size_frame = mu_sigma_result[4][1]
  size_shift = mu_sigma_result[4][2]

  print("preference: {}".format(mu_sigma_result[4]))

# Sound file
SR = 16000
x, _ = librosa.load('ex01/catena.wav', sr=SR)


#
# Step2: Use `Short-time Fourie Transform` to
#   (i)  calculate spectrogram 
#   (ii) conduct speech recognition
#

# preference of frame
hamming_window = np.hamming(size_frame)

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
  cepstrum = np.abs( np.fft.fft(log_abs_spectrum) )

  # extract cepstrum of low index (0~dim & -dim~)
  # cepstrum = np.concatenate([cepstrum[:dim], cepstrum[-dim:]])
  cepstrum = cepstrum[:dim]

  recognition.append( my_models.recognize_word(cepstrum) )


# 
# Draw Figure
#
# preference of figure
fig = plt.figure()
duration = len(x)/SR

# draw spectrogram
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Time [s]')					# x軸のラベルを設定
ax1.set_ylabel('Frequency [Hz]')		# y軸のラベルを設定
ax1.imshow(
	np.flipud(np.array(spectrogram).T),		# 画像とみなすために，データを転置して上下反転
	extent=[0, duration, 0, SR/2],			# (横軸の原点の値，横軸の最大値，縦軸の原点の値，縦軸の最大値)
	aspect='auto',
	interpolation='nearest'
)

# draw speech recognition
ax2 = ax1.twinx()
ax2.set_ylabel('Speech recognition')
x_data = np.linspace(0, duration, len(recognition))
ax2.plot(x_data, recognition, c='b')

plt.title('Spectrogram with speech recognition')
plt.show()

# save as .png file
fig.savefig("ex16/fig/spectrogram_with_recognition_ss{}.png".format(int(SR/size_shift)))