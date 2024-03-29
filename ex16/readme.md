# 演習 16「音声認識」
2 種類の「あいうえお」の一方を用いてモデルを学習し，他方を用いて母音を認識せよ.  
認識された音素の推移をスペクトログラムに並べて(もしくは重ねて)示せ.  
例えば「あ」=0, 「い」=1, 「う」=2, 「え」=3, 「お」=4 とした時系列のグラフにするなど.

- 各母音のケプストラムデータを用いて多次元正規分布を学習
  + 平均ベクトルと共分散行列のパラメータを推定
  + 分散行列は対角成分以外はゼロ
- 認識時には各母音の分布の尤度を算出
  + 尤度が最大の母音を出力

## 方針
- 各音素w（a,i,u,e,o）に対して、音声データのフレーム x_frame がその音である確率を求めるモデル f_w(x_frame) を作る。
  + f_w(x_frame) は正規分布として実装
  + パラメータ μ, Σ を調整する。

- 学習したモデルの保存・読み込みには`pickle`を利用する。
  + cepstrum_model() に渡すパラメータを保存しておく

- 学習データには、自分で録音した音声 `ex02/x.wav` を利用し、テストデータは授業サイトの `aiueo.wav` を利用する。

## files & directories
- `pickle_test`: (directory)
- `learning.py`: パラメータ μ, Σ の学習プログラム
- `speech_recognition.py`: 学習に基づく音声認識をスペクトログラムに表示

## Structure of pickle file
- `mu_sigma_result` (top variable of type list)
  + `words`
  + `mu_result`
  + `Sigma_result`
  + `sigma_elements`