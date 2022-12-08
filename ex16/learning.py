"""
  calculate averege (mu) & covariance matrix (Sigma) for each `ex02/x.wav`.
"""

import pickle
import librosa
import numpy as np

words = ["a", "i", "u", "e", "o"]

# dimention of cepstrum
dim = 13

# list for storing result
mu_result = []
Sigma_result = []
result = [words, mu_result, Sigma_result]


for word in words:

  # load .wav file
  SR = 16000
  x, _ =  librosa.load('ex02/' + word + '.wav', sr=SR)

  # preference of frame
  size_frame = 512
  hamming_window = np.hamming(size_frame)
  size_shift = SR / 100   # 0.01 sec (10 msec)


  # 
  # Step1: `mu`
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
    cepstrum = np.fft.fft(log_abs_spectrum)

    # extract cepstrum of low index (0~dim & -dim~)
    cepstrum = np.concatenate([cepstrum[:dim], cepstrum[-dim:]])
    mu_list.append(cepstrum)

  # average of cepstrum [mu]
  mu = sum(mu_list)/len(mu_list)
  # print("average [mu] for " + word + ": ")
  # print(mu)


  # 
  # Step2: `Sigma`
  # list for storing result
  sigma_sq_list = []

  # calculate sigma^2 for each frame
  for cepstrum in mu_list:
    sigma_sq_list.append( (cepstrum - mu) ** 2 )

  # diagonal elements of Sigma
  sigma_sq = sum(sigma_sq_list)/len(sigma_sq_list)
  # print("diagonal elements of Sigma: ")
  # print(sigma_sq)
  
  # covariance matrix [Sigma]
  Sigma = np.diag(sigma_sq)
  # print("Sigma (size={}):\n{}".format(Sigma.shape, Sigma))


  #
  # Step3: Store result
  mu_result.append(mu)
  Sigma_result.append(Sigma)


# 
# Store results in .pickle file
print("result[0]: {}".format(result[2]))
with open("ex16/mu_sigma_result.pickle", mode="wb") as f:
  pickle.dump(result, f)