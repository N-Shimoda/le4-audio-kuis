import pickle
import numpy as np

"""
  Function to 
  params : x_frame
  return : corresponding value for word
           ([a,i,u,e,o] <--> [0,1,2,3,4])
"""
def recognize_word(cepstrum):

  words = ["a", "i", "u", "e", "o"]
  p_list = []
  
  for word in words:

    p = my_model(cepstrum, word)
    p_list.append(p)

  print("p_list: {}".format(p_list))
  print("type of p_list[0]: {}".format(type(p_list[0])))

  max_p = max(p_list)
  max_index = p_list.index(max_p)

  return max_index


"""
  Function to calculate probability
  params : cepstrum,
           word (a,i,u,e,o)
  return : probability
"""
def my_model(cepstrum, word):

  # dimention of cepstrum
  dim = 13

  # load .pickle file to import parameters
  with open("ex16/mu_sigma_result.pickle", mode="rb") as f:
    mu_sigma_result = pickle.load(f)

  # load [mu] and [Sigma] of given word
  i = mu_sigma_result[0].index(word)
  mu = mu_sigma_result[1][i]
  Sigma = mu_sigma_result[2][i]

  # Calculate probability based on normal distribution
  Sigma_inv = np.linalg.inv(Sigma)
  expo = - (cepstrum - mu).T * Sigma_inv * (cepstrum - mu) / 2      # exponents
  denom = ((2*np.pi) ** (dim/2)) * (np.linalg.det(Sigma) ** 0.5)    # denominator

  p = np.exp(expo) / denom
  return p