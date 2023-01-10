import pickle
import numpy as np

"""
  Function to recognize voice of given frame.
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

  max_p = max(p_list)
  max_index = p_list.index(max_p)

  return max_index


"""
  Function to calculate likelihood of word.
  The more the given "cepstrum" is likely to be the "word", output value becomes greater.
  params : cepstrum,
           word ("a", "i", "u", "e", or "o")
  return : probability
"""
def my_model(cepstrum, word):

  # load .pickle file to import parameters
  with open("ex16/mu_sigma_result.pickle", mode="rb") as f:

    mu_sigma_result = pickle.load(f)

  # load [mu] and [Sigma] of given word
  i = mu_sigma_result[0].index(word)
  mu = mu_sigma_result[1][i]
  Sigma = mu_sigma_result[2][i]
  sigma2_list = mu_sigma_result[3][i]

  """
  # Calculate probability based on normal distribution
  Sigma_inv = np.linalg.inv(Sigma)
  expo = - (cepstrum - mu).T @ Sigma_inv @ (cepstrum - mu) / 2      # exponents
  # print("type of expo = {}".format(type(expo)))
  denom = ((2*np.pi) ** (dim/2)) * (np.linalg.det(Sigma) ** 0.5)    # denominator

  p = np.exp(expo) / denom
  print("p = {}".format(p))
  """

  sigma_list = np.sqrt(sigma2_list)
  L = - sum( np.log(sigma_list) + (cepstrum - mu)**2 / (2*sigma2_list) )

  # print(L)

  return L