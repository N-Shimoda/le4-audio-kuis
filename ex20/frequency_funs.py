"""
  Function to estimate fundamental frequency of a given spectrum
  params : spectrum
  return : f0
"""
def estimate_melody_f0(spectrum):
  pass


"""
  ノートナンバー nn が、与えられたスペクトルにおいて基本周波数である尤度を求める関数
  params : nn
           spectrum
  return : likelihood
"""
def likelihood(nn, spectrum):

  degree = 4
  sub_nn_list = []

  for i in range(0,degree):
    sub_nn_list.append( nn * (i+1) )

  sub_freq_list = 0 ##


# ノートナンバーから周波数へ
def nn2hz(notenum):
	return 440.0 * (2.0 ** ((notenum - 69) / 12.0))