import tkinter as tk
import tkinter.filedialog
import numpy as np
import pyaudio
from gui.left import LeftFrame
from gui.right import RightFrame


class Application(tk.Frame):

  left_frame = None
  right_frame = None
  filename = "mp3/promenade.mp3"
  # filename = None

  # ----- preference -----
  SAMPLING_RATE = 16000
  FRAME_SIZE = 2048
  SHIFT_SIZE = int(SAMPLING_RATE / 20)	# サイズシフト。今回は0.05秒

  # スペクトルをカラー表示する際に色の範囲を正規化するために
  # スペクトルの最小値と最大値を指定
  # スペクトルの値がこの範囲を超えると，同じ色になってしまう
  SPECTRUM_MIN = -5
  SPECTRUM_MAX = 1

  # 音量を表示する際の値の範囲
  VOLUME_MIN = -120
  VOLUME_MAX = -10

  # グラフに表示するデータ数
  MAX_NUM_SPECTROGRAM = int(FRAME_SIZE / 2)   # 縦軸方向
  NUM_DATA_SHOWN = 100                        # 横軸方向

  EPSILON = 1e-10   # log10を計算する際、引数が0にならないようにするためにこの値を足す
  
  # 横軸・縦軸の値のデータ
  time_x_data = np.linspace(0, NUM_DATA_SHOWN * (SHIFT_SIZE/SAMPLING_RATE), NUM_DATA_SHOWN)
  freq_y_data = np.linspace(8000/MAX_NUM_SPECTROGRAM, 8000, MAX_NUM_SPECTROGRAM)

  x_stacked_data = np.array([])
  x_stacked_data_music = np.array([])
  spectrogram_data = None
  spectrogram_data_music = np.zeros((len(freq_y_data), len(time_x_data)))    
  volume_data = None

  hamming_window = np.hamming(FRAME_SIZE)
  stream = None
  now_playing_sec = 0.0
  is_playing = False

  text = None

  
  def __init__(self, master=None):

    # ----- Root frame -----
    super().__init__(master, width=1200, height=800)
    self["bg"]="black"
    self.pack(expand=True, fill="both")
    self.text = tk.StringVar(value='0.0 [s]')   # text needs to be created before `self.create_frames()`

    # ----- Children -----
    self.create_menubar()
    self.create_frames()

    # ----- backend -----
    p = pyaudio.PyAudio()
    self.stream = p.open(
      format = pyaudio.paFloat32,
      channels = 1,
      rate = self.SAMPLING_RATE,
      input = True,						# ここをTrueにするとマイクからの入力になる 
      frames_per_buffer = self.SHIFT_SIZE,		# シフトサイズ
      stream_callback = self._input_callback	# ここでした関数がマイク入力の度に呼び出される（frame_per_bufferで指定した単位で）
    )


  def create_menubar(self):
    
    menubar = tk.Menu(self)
    menu_file = tk.Menu(menubar)
    menubar.add_cascade(label="ファイル", menu=menu_file)
    menu_file.add_command(label="開く...", command=self._menu_file_open, accelerator="Ctrl+o")

    self.master.config(menu=menubar)


  def create_frames(self):

    # ----- destroy current frames -----
    frames = [self.left_frame, self.right_frame]
    for frame in frames:
      if frame is not None:
        frame.destroy()

    # ----- create frames -----
    self.left_frame = LeftFrame(master=self) 
    self.right_frame = RightFrame(master=self)

    self.left_frame.pack(side="left")
    self.right_frame.pack(side="right")

  
  def _menu_file_open(self):

    # stop music player
    self.isPlaying = False

    # update filename via file dialog
    new_filename = tkinter.filedialog.askopenfilename(
      title='Choose .mp3 file',
      filetypes=[("mp3", ".mp3")],
      initialdir="./"
    )

    # update all widgets if any file was selected
    if new_filename != "":
      self.filename = new_filename
      print(self.filename)
      self.create_frames()

  
  # フレーム毎に呼び出される関数
  def _input_callback(self, in_data, frame_count, time_info, status_flags):
    
    # この関数は別スレッドで実行するため
    # メインスレッドで定義した以下の２つの numpy array を利用できるように global 宣言する
    # これらにはフレーム毎のスペクトルと音量のデータが格納される
    # global x_stacked_data, spectrogram_data, volume_data

    # 現在のフレームの音声データをnumpy arrayに変換
    x_current_frame = np.frombuffer(in_data, dtype=np.float32)

    # 現在のフレームとこれまでに入力されたフレームを連結
    self.x_stacked_data = np.concatenate([self.x_stacked_data, x_current_frame])

    # フレームサイズ分のデータがあれば処理を行う
    if len(self.x_stacked_data) >= self.FRAME_SIZE:
      
      # フレームサイズからはみ出した過去のデータは捨てる
      self.x_stacked_data = self.x_stacked_data[len(self.x_stacked_data)-self.FRAME_SIZE:]

      # スペクトルを計算
      fft_spec = np.fft.rfft(self.x_stacked_data * self.hamming_window)
      fft_log_abs_spec = np.log10(np.abs(fft_spec) + self.EPSILON)[:-1]

      # ２次元配列上で列方向（時間軸方向）に１つずらし（戻し）
      # 最後の列（＝最後の時刻のスペクトルがあった位置）に最新のスペクトルデータを挿入
      self.spectrogram_data = np.roll(self.spectrogram_data, -1, axis=1)
      self.spectrogram_data[:, -1] = fft_log_abs_spec

      # 音量も同様の処理
      vol = 20 * np.log10(np.mean(x_current_frame ** 2) + self.EPSILON)
      self.volume_data = np.roll(self.volume_data, -1)
      self.volume_data[-1] = vol
    
    # 戻り値は pyaudio の仕様に従うこと
    return None, pyaudio.paContinue


# ----- main -----
if __name__ == '__main__':

  root = tk.Tk()
  root.title("JoySound")
  app = Application(master=root)
  app.mainloop()