import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import threading
import time
import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks
from gui.volume_view import VolumeView


class RightFrame(tk.Frame):

  info_frame = None
  button_frame = None
  volume_frame = None
  volume_canvas = None
  
  audio_thread = None
  text_thread = None

  audio_data = None
  playing_pos = 0
  calory_text = None
  

  def __init__(self, master=None):

    # ----- Root of left frame -----
    super().__init__(master)
    self.pack(fill="y")

    # ----- Children -----
    self.calory_text = tk.StringVar(value="0.0 kcal")

    self.create_frames()
    self.create_labels()
    self.create_buttons()
    self.create_volume_view()

    # ----- Audiodata (backend) -----
    # pydubを使用して音楽ファイルを読み込む
    if self.master.filename is not None:
      self.audio_data = AudioSegment.from_mp3(self.master.filename)
      self.master.total_time = self.audio_data.duration_seconds
    else:
      self.audio_data = None


  def create_frames(self):
    
    self.info_frame = tk.Frame(
      master=self,
      bd=2,
      relief="raised"
    )
    self.button_frame = tk.Frame(
      master=self,
      bd=2,
      relief="raised"
    )
    self.volume_frame = tk.Frame(
      master=self,
      bd=2,
      relief="raised"
    )

    self.info_frame.pack(expand=True, anchor="s")
    self.button_frame.pack(expand=True, anchor="n")
    self.volume_frame.pack(expand=True, anchor="n")


  def create_labels(self):
    """
    score_label = ttk.Label(
      master=self.info_frame,
      text="96.00",
      font=("Helvetica", "32"),
      relief="raised"
    )
    score_label.pack()
    """

    calory_label = ttk.Label(
      master=self.info_frame,
      textvariable=self.calory_text,
      font=("Helvetica", "32"),
      relief="raised"
    )
    calory_label.pack(anchor="center")

  
  def create_buttons(self):

    play_button = ttk.Button(
      master=self.button_frame,
      text="Play",
      command=self._play_button_Cb
    )
    play_button.pack()


  def create_volume_view(self):

    self.volume_canvas = VolumeView(master=self.volume_frame)
    self.volume_canvas.pack()

    label = ttk.Label(
      master=self.volume_frame,
      text="Volume",
      font=("",16)
    )
    label.pack()


  def _play_button_Cb(self):
    
    if not self.master.is_playing:

      # play audio & update GUI in different threads
      self.audio_thread = threading.Thread(target=self._play_audio)
      self.text_thread = threading.Thread(target=self._update_gui)
      self.audio_thread.setDaemon(True)
      self.text_thread.setDaemon(True)
      
      # set flag as True, and start threads
      self.master.is_playing = True
      self.audio_thread.start()
      self.text_thread.start()

    else:
      self.master.is_playing = False
      self.audio_thread.join()


  def _play_audio(self):

    p = pyaudio.PyAudio()

    # 音声ファイルの再生にはpyaudioを使用
    # ここではpyaudioの再生ストリームを作成
    p_play = pyaudio.PyAudio()
    stream_play = p_play.open(
      format = p.get_format_from_width(self.audio_data.sample_width),	# ストリームを読み書きするときのデータ型
      channels = self.audio_data.channels,							# チャネル数
      rate = self.audio_data.frame_rate,								# サンプリングレート
      output = True   										              # 出力モードに設定
    )


    # この関数は別スレッドで実行するため
    # メインスレッドで定義した以下の２つの変数を利用できるように global 宣言する
    # global is_gui_running, audio_data, now_playing_sec, x_stacked_data_music, spectrogram_data_music

    # pydubのmake_chunksを用いて音楽ファイルのデータを切り出しながら読み込む
    # 第二引数には何ミリ秒毎に読み込むかを指定
    # ここでは10ミリ秒ごとに読み込む

    size_frame_music = 10	# 10ミリ秒毎に読み込む
    idx = self.playing_pos

    # make_chunks関数を使用して一定のフレーム毎に音楽ファイルを読み込む
    #
    # なぜ再生するだけのためにフレーム毎の処理をするのか？
    # 音楽ファイルに対しても何らかの処理を行えるようにするため（このサンプルプログラムでは行っていない）
    # おまけに，再生位置も計算することができる
    for chunk in make_chunks(self.audio_data, size_frame_music):

      # GUIが終了してれば、この関数の処理も終了する
      if self.master.is_playing == False:
        # update playng_pos
        self.playing_pos = idx
        print(self.playing_pos)
        break

      # pyaudioの再生ストリームに切り出した音楽データを流し込む
      # 再生が完了するまで処理はここでブロックされる
      stream_play.write(chunk._data)    # generate sound HERE
      
      # 現在の再生位置を計算（単位は秒）
      self.master.now_playing_sec = (idx * size_frame_music) / 1000.
      idx += 1

      #
      # 【補足】
      # 楽曲のスペクトログラムを計算する場合には下記のように楽曲のデータを受け取る
      # ただし，音声データの値は -1.0~1.0 ではなく，16bit の整数値であるので正規化を施している
      # また十分なサイズの音声データを確保してからfftを実行すること
      # 楽曲が44.1kHzの場合，44100 / (1000/10) のサイズのデータとなる
      # 以下では処理のみを行い，表示はしない．表示をするには animate 関数の中身を変更すること 
      
      # データの取得
      data_music = np.array(chunk.get_array_of_samples())
      
      # 正規化
      data_music = data_music / np.iinfo(np.int32).max	

      #
      # 以下はマイク入力のときと同様
      #

      # 現在のフレームとこれまでに入力されたフレームを連結
      self.master.x_stacked_data_music = np.concatenate([self.master.x_stacked_data_music, data_music])

      # フレームサイズ分のデータがあれば処理を行う
      if len(self.master.x_stacked_data_music) >= self.master.FRAME_SIZE:
        
        # フレームサイズからはみ出した過去のデータは捨てる
        self.master.x_stacked_data_music = self.master.x_stacked_data_music[len(self.master.x_stacked_data_music)-self.master.FRAME_SIZE:]

        # スペクトルを計算
        fft_spec = np.fft.rfft(self.master.x_stacked_data_music * self.master.hamming_window)
        fft_log_abs_spec = np.log10(np.abs(fft_spec) + self.master.EPSILON)[:-1]

        # ２次元配列上で列方向（時間軸方向）に１つずらし（戻し）
        # 最後の列（＝最後の時刻のスペクトルがあった位置）に最新のスペクトルデータを挿入
        self.master.spectrogram_data_music = np.roll(self.master.spectrogram_data_music, -1, axis=1)
        self.master.spectrogram_data_music[:, -1] = fft_log_abs_spec
  

  # function to update GUI of playing time, volume and calory
  def _update_gui(self):

    while True:

      # update playing time & calory
      if self.master.is_playing:
        self.master.text.set( self._generate_playing_time() )
        self.calory_text.set( self._generate_calory(self.master.calory) )

      # update volume plot (always)
      self.volume_canvas.set_volume( self.master.volume_data[-1] )

      # 0.01秒ごとに更新
      time.sleep(0.01)

  
  def _generate_playing_time(self):

    return _seconds2mss(self.master.now_playing_sec) + " / " + _seconds2mss(self.master.total_time)


  def _generate_calory(self, value):

    return "{} kcal".format(round(value,1))


"""
  Function to convert seconds into [m:ss]
  params : seconds
  return : [m:ss]
"""
def _seconds2mss(seconds):

  ss = int(seconds % 60)
  if ss < 10:
    ss = "0{}".format(ss)
  
  result = "{}:{}".format(
    int(seconds // 60),
    ss,
  )

  return result