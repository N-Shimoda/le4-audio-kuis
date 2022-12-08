import matplotlib.pyplot as plt
import numpy as np
import librosa
import pickle

"""
  Function to 
  params : x_frame
  return : estimated cepstrum group?
"""
def recognize_word(x_frame):
  pass


# 
# Step1: Load sound file and parameters
#
# load .wav file
SR = 16000
x, _ = librosa.load('ex16/sound/aiueo.wav', sr=SR)

# load .pickle file
with open("ex16/mu_sigma_result.pickle", mode="rb") as f:
  result = pickle.load(f)

print(result)


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


for i in np.arange(0, len(x)-size_frame, size_shift):
	
	# sound data of current frame
	idx = int(i)
	x_frame = x[idx : idx+size_frame]

  # Calculate spectrum
  fft_spec = np.fft.rfft(x_frame * hamming_window)
  fft_log_abs_spec = np.log(np.abs(fft_spec))
  spectrogram.append(fft_log_abs_spec)
  recognize_word(x_frame)
# 
# Draw Figure
#
# preference of figure
fig = plt.figure()

# draw spectrogram
plt.xlabel('sample')					# x軸のラベルを設定
plt.ylabel('frequency [Hz]')		# y軸のラベルを設定
plt.imshow(
	np.flipud(np.array(spectrogram).T),		# 画像とみなすために，データを転置して上下反転
	extent=[0, len(x), 0, SR/2],			# (横軸の原点の値，横軸の最大値，縦軸の原点の値，縦軸の最大値)
	aspect='auto',
	interpolation='nearest'
)
plt.show()


# save as .png file
fig.savefig('ex16/fig/spectrogram_with_recognition.png')