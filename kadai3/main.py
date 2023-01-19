import tkinter as tk
import tkinter.filedialog
import numpy as np
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

  # グラフに表示する縦軸方向のデータ数
  MAX_NUM_SPECTROGRAM = int(FRAME_SIZE / 2)

  # グラフに表示する横軸方向のデータ数
  NUM_DATA_SHOWN = 100
  
  # 横軸の値のデータ
  time_x_data = np.linspace(0, NUM_DATA_SHOWN * (SHIFT_SIZE/SAMPLING_RATE), NUM_DATA_SHOWN)
  # 縦軸の値のデータ
  freq_y_data = np.linspace(8000/MAX_NUM_SPECTROGRAM, 8000, MAX_NUM_SPECTROGRAM)

  spectrogram_data_music = np.zeros((len(freq_y_data), len(time_x_data)))
  
  
  def __init__(self, master=None):

    # ----- Root frame -----
    super().__init__(master, width=1200, height=800)
    self["bg"]="black"
    self.pack(expand=True, fill="both")

    # ----- Children -----
    self.create_menubar()
    self.create_frames()


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


# ----- main -----
if __name__ == '__main__':

  root = tk.Tk()
  root.title("JoySound")
  app = Application(master=root)
  app.mainloop()