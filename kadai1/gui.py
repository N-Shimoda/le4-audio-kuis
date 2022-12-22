import numpy as np
import matplotlib.pyplot as plt
import tkinter
import pyaudio
import wave
import threading

# MatplotlibをTkinterで使用するために必要
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.process import process_data


def onResize(e):
  # ※ 但し、textウィジェットのwidth,height は文字数指定な点に注意
  # 設定しているフォントサイズにより大きさは異なります。
  if e.widget is root:
    canvas.get_tk_widget().configure(width=e.width//20, height=e.height//20)


def _press_button_play():

  global is_playing
  global my_thread

  if not is_playing:
      is_playing = True
      my_thread = threading.Thread(target=_play_audio)
      my_thread.start()


def _play_audio():

  try:
    wf = wave.open(filename, "r")
  except FileNotFoundError: #ファイルが存在しなかった場合
    print("[Error 404] No such file or directory: " + filename)
    return 0
    
  # ストリームを開く
  p = pyaudio.PyAudio()
  stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                  channels=wf.getnchannels(),
                  rate=wf.getframerate(),
                  output=True)
  # 音声を再生
  chunk = 1024
  data = wf.readframes(chunk)
  while data != '':
    stream.write(data)
    data = wf.readframes(chunk)
  stream.close()
  p.terminate()


def _stop_audio(e):
  pass


def _speech_label(word):
  return "母音 : " + word


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
  label["text"] = _speech_label(words[word_index])


# ----- main -----
#
# Process sound data
filename = 'sound/doppler_trim.wav'
spectrogram, melody, speech, preference = process_data(filename)
[SR, size_frame, size_shift, duration] = preference

is_playing = False
my_thread = None


# Tkinterを初期化
root = tkinter.Tk()

root.wm_title("EXP4-AUDIO-GUI")
# root.bind("<Configure>", onResize)
root.geometry("800x1200")

frame0 = tkinter.Frame(root, relief="solid", bd=3)
frame1 = tkinter.Frame(root, relief="solid", bd=3)
frame2 = tkinter.Frame(root, relief="solid", bd=3)
frame0.grid(column=0, row=0, columnspan=2)
frame1.grid(column=0, row=1, sticky="NS")
frame2.grid(column=1, row=1)


#
# Frame0
#

play_button = tkinter.Button(frame0, text="PLAY", command=_press_button_play, bg="red")
play_button.grid(column=0, row=0)

stop_button = tkinter.Button(
  frame0,
  text="STOP",
  bg="gray"
)
stop_button.grid(column=1, row=0)
stop_button.bind("<ButtonPress>", _stop_audio)


#
# Frame1
#

#
# Show filename
file_label = tkinter.Label(
  frame1,
  text=filename,
  fg="black",
  bg="white",
  font=("", 30)
)
file_label.grid()


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

canvas.get_tk_widget().grid()
canvas.get_tk_widget().configure(width=720, height=700)

# 
# Slide bar
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
	font=("", 20),				# フォントサイズは20pxに設定
  bg="white"
)
scale.grid()


#
# Frame2

# スペクトルを表示する領域を確保
# ax2, canvs2 を使って上記のコールバック関数でグラフを描画する
fig2, ax2 = plt.subplots()
canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
canvas2.get_tk_widget().grid()
canvas2.get_tk_widget().configure(width=720, height=800)

#
# Recognized voice
label = tkinter.Label(
  frame2,
  text = _speech_label("(未選択)"),
  fg="red",
  bg="white",
  font=("", 40)
)
label.grid()


#
# TkinterのGUI表示を開始
tkinter.mainloop()