import numpy as np
import math

# 周波数からノートナンバーへ変換（notenumber.pyより）
def hz2nn(frequency):
	return int (round (12.0 * (math.log(frequency / 440.0) / math.log (2.0)))) + 69


"""
  スペクトルと対応する周波数ビンの情報を受け取り，クロマベクトルを算出
  params : spectrum
           frequencies
           nn_range       [int list]
  return : chroma vector  [int list]  (length=12)
"""
def chroma_vector(spectrum, frequencies):
  # 0 = C, 1 = C#, 2 = D, ..., 11 = B
	# 12次元のクロマベクトルを作成（ゼロベクトルで初期化）
  cv = np.zeros(12)
  
  # スペクトルの周波数ビン毎に
  # クロマベクトルの対応する要素に振幅スペクトルを足しこむ
  for s, f in zip (spectrum , frequencies):
    nn = hz2nn(f)
    cv[nn % 12] += np.abs(s)
    
  return cv