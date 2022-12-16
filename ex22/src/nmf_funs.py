import numpy as np

"""
  Function to apply NMF to given matrix. 
  params : spectrum (matrix)  [np.array]
           k                  [int]
           epoc               [int]
  return : H,U
"""
def apply_nmf(spectrum, k, epoc):

  # input array as matrix
  Y = spectrum
  print("shape of input array: {}".format(Y.shape))
  
  # verify the value of k
  if k > Y.shape[0] or k > Y.shape[1]:
    raise Exception("variable k exception")

  # initialize H,U
  H = np.random.rand(Y.shape[0], k)
  U = np.random.rand(k, Y.shape[1])

  # learning process
  for i in range(epoc):
    print("{}th generation".format(i))
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

      denom = np.sum( U[k] * np.dot(H[n],U) )   # denominator
      num = np.sum(Y[n] * U[k])               # numerator
      newH[n][k] = H[n][k] * (num/denom)

  # update U
  for k in range(U.shape[0]):
    for m in range(U.shape[1]):

      vec = U[:,m].reshape(-1,1)
      denom = np.sum( np.dot(newH[:,k], np.dot(newH,vec)) )   # denominator
      num = np.sum(Y[:,m] * newH[:,k])                           # numerator
      newU[k][m] = U[k][m] * (num/denom)

  return newH, newU