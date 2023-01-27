import tkinter as tk
import tkinter.ttk as ttk
import numpy as np

# matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class LeftFrame(tk.Frame):

  draw_frame = None
  tabbar_frame = None
  ax1_sub = None
  ax2_sub = None
  ani = None

  time_label = None

  NN_MIN = 0
  NN_MAX = 12


  def __init__(self, master=None):

    # ----- Root of left frame -----
    super().__init__(master)
    self.pack(expand=True, fill="both")

    # ----- Children -----
    self.create_frames()
    self.create_canvas()
    self.create_tabbar()


  def create_frames(self):

    self.draw_frame = tk.Frame(
      master=self,
      bd=2,
      relief="raised"
    )
    self.draw_frame.pack(expand=True, fill="both")

    self.tabbar_frame = tk.Frame(
      master=self,
      bd=2,
      relief="raised"
    )
    self.tabbar_frame.pack(fill="x")


  def create_canvas(self):

    # ----- draw canvas -----
    fig, ax1 = plt.subplots(1, 1)
    canvas = FigureCanvasTkAgg(fig, master=self.draw_frame)

    # とりあえず初期値（ゼロ）のスペクトログラムと音量のデータを作成
    # この numpy array にデータが更新されていく
    self.master.spectrogram_data = np.zeros((len(self.master.freq_y_data), len(self.master.time_x_data)))

    # 楽曲のスペクトログラムを格納するデータ（このサンプルでは計算のみ）
    self.master.spectrogram_data_music = np.zeros((len(self.master.freq_y_data), len(self.master.time_x_data)))

    # スペクトログラムを描画する際に横軸と縦軸のデータを行列にしておく必要がある
    # これは下記の matplotlib の pcolormesh の仕様のため
    X = np.zeros(self.master.spectrogram_data_music.shape)
    Y = np.zeros(self.master.spectrogram_data_music.shape)
    for idx_f, f_v in enumerate(self.master.freq_y_data):
      for idx_t, t_v in enumerate(self.master.time_x_data):
        X[idx_f, idx_t] = t_v
        Y[idx_f, idx_t] = f_v

    # pcolormeshを用いてスペクトログラムを描画
    # 戻り値はデータの更新 & 再描画のために必要
    self.ax1_sub = ax1.pcolormesh(
      X,
      Y,
      self.master.spectrogram_data_music,
      shading='nearest',	# 描画スタイル
      cmap='jet',			# カラーマップ
      norm=Normalize(self.master.SPECTRUM_MIN, self.master.SPECTRUM_MAX)	# 値の最小値と最大値を指定して，それに色を合わせる
    )

    # 音量を表示するために反転した軸を作成
    ax2 = ax1.twinx()

    # 音量をプロットする
    # 戻り値はデータの更新 & 再描画のために必要
    # self.ax2_sub, = ax2.plot(self.master.time_x_data, self.master.volume_data, c='y')
    self.ax2_sub, = ax2.plot(self.master.time_x_data, self.master.pitch_data, c='black')

    # ラベルの設定
    ax1.set_xlabel('sec')				      # x軸のラベルを設定
    ax1.set_ylabel('frequency [Hz]')	# y軸のラベルを設定
    ax2.set_ylabel('note number')		  # 反対側のy軸のラベルを設定

    # 音量を表示する際の値の範囲を設定
    # ax2.set_ylim([self.master.VOLUME_MIN, self.master.VOLUME_MAX])
    ax2.set_ylim([self.NN_MIN, self.NN_MAX])

    # maplotlib animationを設定
    # if self.ax1_sub is not None:
    self.ani = animation.FuncAnimation(
      fig,
      self._animate,		# 再描画のために呼び出される関数
      interval=100,	    # 100ミリ秒間隔で再描画を行う（PC環境によって処理が追いつかない場合はこの値を大きくするとよい）
      blit=True		      # blitting処理を行うため描画処理が速くなる
    )

    # matplotlib を GUI(Tkinter) に追加する
    # toolbar = NavigationToolbar2Tk(canvas, self.draw_frame)
    canvas.get_tk_widget().pack(expand=True, fill="both")


  def create_tabbar(self):

    # label to show playing time
    self.time_label = tk.Label(
      master=self.tabbar_frame,
      textvariable=self.master.text,
      font=("Helvetica", 16)
    )
    self.time_label.pack(anchor="w")

    """
    # scale (tabbar) to show playing time
    var_scale_ttk = tk.DoubleVar()
    scale = ttk.Scale(
      master=self.tabbar_frame,
      variable=var_scale_ttk,
      length=200
    )
    scale.pack()
    """


  # matplotlib animation によって呼び出される関数
  # ここでは最新のスペクトログラムと音量のデータを格納する
  # 再描画はmatplotlib animationが行う
  def _animate(self, frame_index):

    self.ax1_sub.set_array(self.master.spectrogram_data)
    # ax1_sub.set_array(spectrogram_data_music)   # このようにすれば楽曲のスペクトログラムが表示される
    
    # self.ax2_sub.set_data(self.master.time_x_data, self.master.volume_data)
    self.ax2_sub.set_data(self.master.time_x_data, self.master.pitch_data)
    
    return self.ax1_sub, self.ax2_sub