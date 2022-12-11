"""
  Exercise 20 "Melody Recognition"
  input  : sound data [.wav]
  output : pitch of recognized melody shown as a graph [.png]
"""

import matplotlib.pyplot as plt
import numpy as np
import librosa
from chroma_funs import chroma_vector
from melody_funs import estimate_melody_f0


# Load sound file
SR = 16000
x, _ = librosa.load('sound/shs-test-man.wav', sr=SR)

# list for storing results
# spectrogram = []
# chromagram = []
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
  # spectrogram.append(fft_log_abs_spec)

  """
  # Chroma vector
  freq = np.linspace(8000/len(fft_spec), 8000, len(fft_spec))
  cv = chroma_vector(fft_spec, freq)    # cv : float64 ndarray (length=12)
  chromagram.append(cv)
  """

  # Estimate frequency of melody
  nn_range = np.arange(37,60)   # range of note number
  melody_nn, melody_f0 = estimate_melody_f0(nn_range, fft_log_abs_spec, SR)
  melody.append(melody_nn)


# 
# Draw Figure
#
fig, ax = plt.subplots()

# ax.plot(melody)
ax.plot(melody)
ax.set_xlabel('time [s]')
ax.set_ylabel('melody [Hz]')
ax.grid()

plt.title('Estimated melody')
plt.show()

fig.savefig("ex20/fig/estimated_melody.png")