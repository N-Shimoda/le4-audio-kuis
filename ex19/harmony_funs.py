import numpy as np

"""
  Function to estimate harmony from chroma vector
  return : [type, root]   (type = 0,1,   root = 0~11)
"""
def estimate_harmony(cv):

  types = [0, 1]    # major & minor
  roots = range(0,12)

  # list of probability
  p_list = []

  # calculate likelihood for 24 patterns
  for type in types:
    for root in roots:
      p = likelihood(cv, root, type)
      p_list.append(p)
    

  # return the pattern which corresponds to max value
  # major=0, minor=1
  index = p_list.index( max(p_list) )
  type = index // 12
  root = index % 12

  return [type, root]


"""
  params : cv     (chroma vector)       [ndarray of float64],
           root   (0 ~ 11)              [int]
           type   (0 or 1)              [int]
  return : likelihood                   [float64]
"""
def likelihood(cv, root, type):

  # weight
  a = np.array([1.0, 0.5, 0.8])

  if type == 0:
    notes = list(map(lambda n: n%12, [root, root+4, root+7]))
  else:
    notes = list(map(lambda n: n%12, [root, root+3, root+7]))

  # `chroma vector` value for each notes
  cv_notes = np.array( list(map(lambda c: cv[c], notes)) )

  return sum(a * cv_notes)