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
    spectrogram_data = np.zeros((len(self.master.freq_y_data), len(self.master.time_x_data)))
    volume_data = np.zeros(len(self.master.time_x_data))

    # 楽曲のスペクトログラムを格納するデータ（このサンプルでは計算のみ）
    spectrogram_data_music = np.zeros((len(self.master.freq_y_data), len(self.master.time_x_data)))

    # スペクトログラムを描画する際に横軸と縦軸のデータを行列にしておく必要がある
    # これは下記の matplotlib の pcolormesh の仕様のため
    X = np.zeros(spectrogram_data.shape)
    Y = np.zeros(spectrogram_data.shape)
    for idx_f, f_v in enumerate(self.master.freq_y_data):
      for idx_t, t_v in enumerate(self.master.time_x_data):
        X[idx_f, idx_t] = t_v
        Y[idx_f, idx_t] = f_v

    # pcolormeshを用いてスペクトログラムを描画
    # 戻り値はデータの更新 & 再描画のために必要
    ax1_sub = ax1.pcolormesh(
      X,
      Y,
      spectrogram_data,
      shading='nearest',	# 描画スタイル
      cmap='jet',			# カラーマップ
      norm=Normalize(self.master.SPECTRUM_MIN, self.master.SPECTRUM_MAX)	# 値の最小値と最大値を指定して，それに色を合わせる
    )

    # 音量を表示するために反転した軸を作成
    ax2 = ax1.twinx()

    # 音量をプロットする
    # 戻り値はデータの更新 & 再描画のために必要
    ax2_sub, = ax2.plot(self.master.time_x_data, volume_data, c='y')

    # ラベルの設定
    ax1.set_xlabel('sec')				# x軸のラベルを設定
    ax1.set_ylabel('frequency [Hz]')	# y軸のラベルを設定
    ax2.set_ylabel('volume [dB]')		# 反対側のy軸のラベルを設定

    # 音量を表示する際の値の範囲を設定
    ax2.set_ylim([self.master.VOLUME_MIN, self.master.VOLUME_MAX])

    """

    # maplotlib animationを設定
    ani = animation.FuncAnimation(
      fig,
      self._animate,		# 再描画のために呼び出される関数
      interval=100,	# 100ミリ秒間隔で再描画を行う（PC環境によって処理が追いつかない場合はこの値を大きくするとよい）
      blit=True		# blitting処理を行うため描画処理が速くなる
    )
    """

    # matplotlib を GUI(Tkinter) に追加する
    toolbar = NavigationToolbar2Tk(canvas, self.draw_frame)
    canvas.get_tk_widget().pack(expand=True, fill="both")


  def create_tabbar(self):

    time_label = ttk.Label(
      master=self.tabbar_frame,
      text="3:34 / 4:55",
      font=("naonao", 16)
    )
    time_label.pack(anchor="w")

    var_scale_ttk = tk.DoubleVar()
    scale = ttk.Scale(
      master=self.tabbar_frame,
      variable=var_scale_ttk,
      length=200
    )
    scale.pack()


  # matplotlib animation によって呼び出される関数
  # ここでは最新のスペクトログラムと音量のデータを格納する
  # 再描画はmatplotlib animationが行う
  """
  def _animate(self, frame_index, ax1_sub, ax2_sub):

    ax1_sub.set_array(spectrogram_data)

    # この上の処理を下記のようにすれば楽曲のスペクトログラムが表示される
    # ax1_sub.set_array(spectrogram_data_music)
    
    ax2_sub.set_data(time_x_data, volume_data)
    
    return ax1_sub, ax2_sub
  """ 