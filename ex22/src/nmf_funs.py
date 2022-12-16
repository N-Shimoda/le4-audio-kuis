import numpy as np

"""
  Function to apply NMF to given matrix. 
  params : spectrum (matrix)  [ndarray list]
           k                  [int]
  return : H,U
"""
def apply_nmf(spectrum, k):

  # input array as matrix
  Y = np.array(spectrum)
  
  # verify the value of k
  if k > Y.shape[0] or k > Y.shape[1]:
    raise Exception("variable k exception")

  # initialize H,U
  H = np.ones((Y.shape[0], k))
  U = np.ones((k, Y.shape[1]))

  # learning process
  upper = 100
  for i in range(upper):
    H, U = get_next(Y,H,U)

  return H, U


"""
  Function to update NMF results (H and U), using Auxiliary Function Method.
  For more detailes, see equation (35),(36) in the textbook.
  params : H, U
  return : newH, newU
"""
def get_next(Y, H, U):

  newH = np.zeros(H.shape)
  newU = np.zeros(U.shape)

  # update H
  for n in range(H.shape[0]):
    for k in range(H.shape[1]):

      denom = sum(U[k] * sum(H[n]*U.T))   # denominator
      num = sum(Y[n] * U[k])              # numerator
      newH[n][k] = H[n][k] * (num/denom)

  # update U
  for k in range(U.shape[0]):
    for m in range(U.shape[1]):

      denom = sum(H.T[k] * sum(H[n]*U.T))   # denominator
      num = sum(Y[n] * U[k])                # numerator
      newU[k][m] = U[k][m] * (num/denom)

  return newH, newU