import librosa
import numpy as np
import matplotlib.pyplot as plt
import pickle
from src.nmf_funs import apply_nmf

# 
# Load sound file
SR = 16000
src_path = 'sound/nmf_piano_sample.wav'
x, _ = librosa.load(src_path, sr=SR)
duration = len(x)/SR    # file size
print(">> File loaded from '{}'".format(src_path))


# 
# Step1: Convert sound data into spectrum
spectrum = []

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
  fft_abs_spec = np.abs(fft_spec)
  spectrum.append(fft_abs_spec)


#
# Step2: Apply NMF (Non-negative Matrix Factorizaion) to `spectrum`
k = 2
epoc = 50
spectrum_array = np.array(spectrum).T
H, U = apply_nmf(spectrum_array, k, epoc)

print("H (shape={}):\n{}\n".format(H.shape, H))
print("U (shape={}):\n{}\n".format(U.shape, U))

# store result in .pickle file
with open("ex22/cache/results.pickle", mode="wb") as f:
  result = [H,U]
  pickle.dump(result, f)


#
# Step3: Show result [U] as spectrogram
fig = plt.figure()

# H
ax1 = fig.add_subplot(1,2,1)
ax1.set_xlabel('sound source')
ax1.set_ylabel('frequency [Hz]')
#  ax1.plot(H)
ax1.imshow(
  np.flipud(H),
  extent=[0, len(x), 0, 16000/2],
  aspect='auto',
	interpolation='nearest'
)

# U
ax2 = fig.add_subplot(1,2,2)
ax2.set_xlabel('sec')
ax2.set_ylabel('sound source')
ax2.imshow(
  U,
  aspect='auto',
  interpolation='nearest'
)

plt.show()
fig.savefig('ex22/fig/nmf_result_k={}_epoc={}_.png'.format(k, epoc))