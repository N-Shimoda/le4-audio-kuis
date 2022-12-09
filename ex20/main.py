import matplotlib.pyplot as plt
import numpy as np
import librosa
from chroma_funs import chroma_vector
from frequency_funs import estimate_melody_f0

# Load sound file
SR = 16000
x, _ = librosa.load('sound/shs-test-man.wav', sr=SR)

# list for storing results
spectrogram = []
chromagram = []
melody = []


#
# calculate spectrum & chroma-vector for each frames
#

# preference of frame
size_frame = 2048
size_shift = SR / 100
hamming_window = np.hamming(size_frame)

# divide data into frames
for i in np.arange(0, len(x)-size_frame, size_shift):

  # sound data of current frame
  idx = int(i)
  x_frame = x[idx : idx+size_frame]

  # Spectrum
  fft_spec = np.fft.rfft(x_frame * hamming_window)
  fft_log_abs_spec = np.log(np.abs(fft_spec))
  spectrogram.append(fft_log_abs_spec)

  # Chroma vector
  freq = np.linspace(8000/len(fft_spec), 8000, len(fft_spec))
  nn_range = range(36,61)                         # range of note number
  cv = chroma_vector(fft_spec, freq)    # cv : float64 ndarray (length=12)
  chromagram.append(cv)

  # Estimate frequency of melody
  melody_f0 = estimate_melody_f0(fft_spec)
  melody.append(melody_f0)


# 
# Draw Figure
#

# preference
fig = plt.figure()

# draw chromagram
ax1 = fig.add_subplot(111)
ax1.set_xlabel('time [s]')					# x軸のラベルを設定
ax1.set_ylabel('note number')		# y軸のラベルを設定
ax1.imshow(
	np.flipud(np.array(chromagram).T),		# 画像とみなすために，データを転置して上下反転
	aspect='auto',
	interpolation='nearest'
)

# draw estimated pitch
ax2 = ax1.twinx()
ax2.set_ylabel('f0')
ax2.plot(melody, c='w')

# show picture and save as .png file
plt.show()
fig.savefig("ex20/fig/pitch.png")