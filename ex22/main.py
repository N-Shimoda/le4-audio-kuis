import librosa
import numpy as np
import matplotlib.pyplot as plt
from src.nmf_funs import apply_nmf

# 
# Load sound file
SR = 16000
src_path = 'sound/kimigayo_trim.wav'
x, _ = librosa.load(src_path, sr=SR)
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

print(len(spectrum))


#
# Step2: Apply NMF (Non-negative Matrix Factorizaion) to `spectrum`
k = 20
H, U = apply_nmf(spectrum, k)


#
# Step3: Show result [U] as spectrogram
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.set_xlabel('sec')
ax1.set_ylabel('elements (K)')
ax1.plot(U)

fig.show()
fig.savefig('ex22/fig/nmf_result.png')