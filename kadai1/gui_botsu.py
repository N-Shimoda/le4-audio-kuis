import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import src.my_funs as tools


def plot_spectrogram(frame, spectrogram):

  # duration = len(spectrogram)/16000  # ??
  duration = 0

  # まずはスペクトログラムを描画
  fig, ax = plt.subplots()
  canvas = FigureCanvasTkAgg(fig, master=frame)	# masterに対象とするframeを指定
  plt.xlabel('sec')
  plt.ylabel('frequency [Hz]')
  plt.imshow(
    np.flipud(np.array(spectrogram).T),
    extent=[0, duration, 0, 8000],
    aspect='auto',
    interpolation='nearest'
  )
  canvas.get_tk_widget().pack(side="left")	# 最後にFrameに追加する処理


def main():

  root = tk.Tk()
  root.title("Sound Wave GUI")

  # frame1
  frame1 = tk.Frame(root)
  label1 = tk.Label(frame1, relief=tk.SOLID, text="frame1")
  label1.pack()

  spectrogram = tools.getSpectrogram()
  plot_spectrogram(frame1, spectrogram)


  # frame2
  frame2 = tk.Frame(root)
  label2 = tk.Label(frame2, relief=tk.SOLID, text="frame2")
  label2.pack()

  frame1.pack(side="left")
  frame2.pack(side="right")

  tk.mainloop()





main()