"""
  calculate averege (mu) & covariance matrix (Sigma) for each `ex02/x.wav`.
"""

import pickle
import librosa
import numpy as np


# dimention of cepstrum
dim = 18
words = ["a", "i", "u", "e", "o"]


# list for storing result
mu_result = []
Sigma_result = []
sigma_elements = []
result = [words, mu_result, Sigma_result, sigma_elements, dim]


for word in words:

  # load .wav file
  SR = 16000
  x, _ =  librosa.load('ex02/' + word + '.wav', sr=SR)

  # preference of frame
  size_frame = 256
  hamming_window = np.hamming(size_frame)
  size_shift = SR / 100   # 0.01 sec (10 msec)


  # 
  # Step1: `mu`
  #
  # list for storing result
  mu_list = []

  # calculate cepstrum in each frame
  for i in np.arange(0, len(x)-size_frame, size_shift):

    # sound data of current frame
    idx = int(i)
    x_frame = x[idx : idx+size_frame] * hamming_window

    # calculate cepstrum
    amp_spectrum = np.fft.rfft(x_frame)
    log_abs_spectrum = np.log( np.abs(amp_spectrum) )
    cepstrum = np.abs( np.fft.fft(log_abs_spectrum) )

    # extract cepstrum of low index (0~dim & -dim~)
    # cepstrum = np.concatenate([cepstrum[:dim], cepstrum[-dim:]])
    cepstrum = cepstrum[:dim]
    mu_list.append(cepstrum)

  # average of cepstrum [mu]
  mu = sum(mu_list)/len(mu_list)
  # print("average [mu] for " + word + ": ")
  # print(mu)


  # 
  # Step2: `Sigma`
  #
  # list for storing result
  sigma_sq_list = []    # matrix

  # calculate sigma^2 for each frame
  for cepstrum in mu_list:
    sigma_sq_list.append( (cepstrum - mu) ** 2 )

  # diagonal elements of Sigma
  sigma_sq = sum(sigma_sq_list)/len(sigma_sq_list)
  
  # covariance matrix [Sigma]
  Sigma = np.diag(sigma_sq)
  # print("Sigma (size={}):\n{}".format(Sigma.shape, Sigma))


  #
  # Step3: Store result
  #
  mu_result.append(mu)
  Sigma_result.append(Sigma)
  sigma_elements.append(sigma_sq)


# 
# Save results in .pickle file
#
print("dimention: {}".format(result[4]))

with open("ex16/mu_sigma_result.pickle", mode="wb") as f:

  pickle.dump(result, f)

print(">> File written in pickle file.")