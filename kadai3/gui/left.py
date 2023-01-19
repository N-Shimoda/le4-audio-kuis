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

    # ----- preference -----
    # サンプリングレート
    SAMPLING_RATE = 16000

    # フレームサイズ
    FRAME_SIZE = 2048

    # サイズシフト
    SHIFT_SIZE = int(SAMPLING_RATE / 20)	# 今回は0.05秒

    # スペクトルをカラー表示する際に色の範囲を正規化するために
    # スペクトルの最小値と最大値を指定
    # スペクトルの値がこの範囲を超えると，同じ色になってしまう
    SPECTRUM_MIN = -5
    SPECTRUM_MAX = 1

    # 音量を表示する際の値の範囲
    VOLUME_MIN = -120
    VOLUME_MAX = -10

    """
    # log10を計算する際、引数が0にならないようにするためにこの値を足す
    # EPSILON = 1e-10

    # ハミング窓
    hamming_window = np.hamming(FRAME_SIZE)
    """

    # グラフに表示する縦軸方向のデータ数
    MAX_NUM_SPECTROGRAM = int(FRAME_SIZE / 2)

    # グラフに表示する横軸方向のデータ数
    NUM_DATA_SHOWN = 100


    # ----- draw canvas -----
    fig, ax1 = plt.subplots(1, 1)
    canvas = FigureCanvasTkAgg(fig, master=self.draw_frame)

    # 横軸の値のデータ
    time_x_data = np.linspace(0, NUM_DATA_SHOWN * (SHIFT_SIZE/SAMPLING_RATE), NUM_DATA_SHOWN)
    # 縦軸の値のデータ
    freq_y_data = np.linspace(8000/MAX_NUM_SPECTROGRAM, 8000, MAX_NUM_SPECTROGRAM)

    # とりあえず初期値（ゼロ）のスペクトログラムと音量のデータを作成
    # この numpy array にデータが更新されていく
    spectrogram_data = np.zeros((len(freq_y_data), len(time_x_data)))
    volume_data = np.zeros(len(time_x_data))

    # 楽曲のスペクトログラムを格納するデータ（このサンプルでは計算のみ）
    spectrogram_data_music = np.zeros((len(freq_y_data), len(time_x_data)))

    # スペクトログラムを描画する際に横軸と縦軸のデータを行列にしておく必要がある
    # これは下記の matplotlib の pcolormesh の仕様のため
    X = np.zeros(spectrogram_data.shape)
    Y = np.zeros(spectrogram_data.shape)
    for idx_f, f_v in enumerate(freq_y_data):
      for idx_t, t_v in enumerate(time_x_data):
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
      norm=Normalize(SPECTRUM_MIN, SPECTRUM_MAX)	# 値の最小値と最大値を指定して，それに色を合わせる
    )

    # 音量を表示するために反転した軸を作成
    ax2 = ax1.twinx()

    # 音量をプロットする
    # 戻り値はデータの更新 & 再描画のために必要
    ax2_sub, = ax2.plot(time_x_data, volume_data, c='y')

    # ラベルの設定
    ax1.set_xlabel('sec')				# x軸のラベルを設定
    ax1.set_ylabel('frequency [Hz]')	# y軸のラベルを設定
    ax2.set_ylabel('volume [dB]')		# 反対側のy軸のラベルを設定

    # 音量を表示する際の値の範囲を設定
    ax2.set_ylim([VOLUME_MIN, VOLUME_MAX])

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