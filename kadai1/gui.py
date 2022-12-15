#
# 計算機科学実験及演習 4「音響信号処理」
# サンプルソースコード
#
# 音声ファイルを読み込みスペクトログラムを表示する
# その隣に時間を選択するスライドバーと選択した時間に対応したスペクトルを表示する
# GUIのツールとしてTkinterを使用する
#

# ライブラリの読み込み
import numpy as np
import matplotlib.pyplot as plt
import tkinter

# MatplotlibをTkinterで使用するために必要
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.process import process_data


# スライドバーの値が変更されたときに呼び出されるコールバック関数
# ここで右側のグラフに
# vはスライドバーの値
def _tabbar_Cb(v):

  # Acquire index and corresponding data
  # スライドバーの値からスペクトルのインデクスおよびそのスペクトルを取得
  index = int((len(spectrogram)-1) * (float(v) / duration))
  spectrum = spectrogram[index]
  word_index = speech[index]

  # Update selected position
  vline.set_xdata(float(v))
  canvas.draw()
  
  # Update spectrogram
  # 直前のスペクトル描画を削除し，新たなスペクトルを描画
  plt.cla()
  x_data = np.fft.rfftfreq(size_frame, d=1/SR)
  ax2.plot(x_data, spectrum)
  ax2.set_ylim(-10, 5)
  ax2.set_xlim(0, SR/2)
  ax2.set_ylabel('amblitude')
  ax2.set_xlabel('frequency [Hz]')
  canvas2.draw()

  # Update speech recognition
  words = ["あ","い","う","え","お"]
  label["text"] = words[word_index]


#
# Process sound data
filename = 'sound/aiueo.wav'
spectrogram, melody, speech, preference = process_data(filename)
[SR, size_frame, size_shift, duration] = preference


# Tkinterを初期化
root = tkinter.Tk()
root.wm_title("EXP4-AUDIO-SAMPLE")

#
# Frame1
frame1 = tkinter.Frame(root)

# 
# Draw spectrogram & Melody
fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, master=frame1)	# masterに対象とするframeを指定

# spectrogram
ax1 = fig.add_subplot(111)
ax1.set_xlabel('sec')
ax1.set_ylabel('frequency [Hz]')
ax1.imshow(
	np.flipud(np.array(spectrogram).T),
	extent=[0, duration, 0, 8000],
	aspect='auto',
	interpolation='nearest'
)

# fundamental frequency (f0)
ax2 = ax1.twinx()
ax2.set_ylabel('f0 frequency [Hz]')
x_data = np.linspace(0, duration, len(melody))
ax2.plot(x_data, melody, c='y')

# vertical line of selected position
vline = ax1.axvline(x=0, color='red')

canvas.get_tk_widget().pack()


# 
# Create slide bar
scale = tkinter.Scale(
	command=_tabbar_Cb,		# ここにコールバック関数を指定
	master=frame1,				# 表示するフレーム
	from_=0,					# 最小値
	to=duration,				# 最大値
	resolution=size_shift/SR,	# 刻み幅
  variable=0.0,
	label=u'スペクトルを表示する時間[sec]',
	orient=tkinter.HORIZONTAL,	# 横方向にスライド
	length=600,					# 横サイズ
	width=50,					# 縦サイズ
	font=("", 20)				# フォントサイズは20pxに設定
)
scale.pack()


#
# Frame2
frame2 = tkinter.Frame(root)

# スペクトルを表示する領域を確保
# ax2, canvs2 を使って上記のコールバック関数でグラフを描画する
fig2, ax2 = plt.subplots()
canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
canvas2.get_tk_widget().pack(side="top")	# "top"は上部方向にウィジェットを積むことを意味する

#
# Recognized voice
recognized_word = "あ"
label = tkinter.Label(
  frame2,
  text="母音 : "+recognized_word,
  fg="red",
  font=("", 40)
)
label.pack()


#
# TkinterのGUI表示を開始
frame1.pack(side="left", expand=True)
frame2.pack(side="right", expand=True)
tkinter.mainloop()