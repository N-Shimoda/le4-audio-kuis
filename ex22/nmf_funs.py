import numpy as np

"""
  Function to apply NMF to given matrix. 
  params : spectrum (matrix)  [ndarray list]
           k
  return : H,U
"""
def apply_nmf(spectrum, k):

  # input matrix
  Y = np.array(spectrum)
  
  if k > Y.shape[0] or k > Y.shape[1]:
    raise Exception("variable k exception")

  # initialize H,U
  H = np.ones((Y.shape[0], k))
  U = np.ones((k, Y.shape[1]))

  diff_rate = 100

  # learning process
  while diff_rate > 1:
    new_H, new_U = get_next(H,U)
    diff_rate = get_diff_rate(H, U, new_H, new_U)

    H = new_H
    U = new_U

  return H, U


def get_next(H,U):
  pass


def get_diff_rate(H, U, new_H, new_U):
  pass