# Same function as ex21

"""
  Function to estimate fundamental frequency of a given spectrum
  params : nn_range     (candidates of f0)        [int list]
           log_abs_spec (log amplitude spectrum)  [ndarray, length=1025]
           SR           (sampling rate)           [int]
  return : max_nn       (notenumber of melody)    [int]
           f0           (frequency of melody)     [float]
"""
def estimate_melody_f0(nn_range, log_abs_spec, SR):

  L_list = []

  # calculate likelihood for each note numbers
  for nn in nn_range:

    L_list.append(likelihood(nn, log_abs_spec, SR))

  max_index = L_list.index( max(L_list) )
  max_nn = nn_range[max_index]
  f0 = nn2hz(max_nn)

  return max_nn, f0


"""
  ノートナンバー nn が、与えられたスペクトルにおいて基本周波数である尤度を求める関数
  params : nn            (note number)             [int]
           log_abs_spec  (log amplitude spectrum)  [ndarray, length=1025]
  return : likelihood
"""
def likelihood(nn, log_abs_spec, SR):

  #
  # Calculate frequency of sub harmonies
  degree = 4    # length of subharmony
  sub_nn_list = []

  for i in range(0,degree):
    sub_nn_list.append( nn + i*12 )

  sub_harmonies = list(map(nn2hz, sub_nn_list))


  #
  # Calculate lilkelihood
  L = 0
  
  for freq in sub_harmonies:
    spec_index = int(freq/(SR/2) * len(log_abs_spec))
    # print("spec_index: {}".format(spec_index))
    # print("log_abs_spec[spec_index] = {}".format(log_abs_spec[spec_index]))
    L += log_abs_spec[spec_index]
  
  return L


"""
  Function to convert note number into frequency.
  params : notenum    [float]  ** usualy given as int **
  return : frequency  [float (hz)]
"""
def nn2hz(notenum):
	return 440.0 * (2.0 ** ((notenum - 69) / 12.0))