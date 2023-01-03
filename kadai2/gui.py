import tkinter as tk
import tkinter.filedialog
import matplotlib.pyplot as plt
import numpy as np
import threading
import os
import wave
import pyaudio

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.process import process_data


# class 'Application' inherits tk.Frame
class Application(tk.Frame):

  filename = "/Users/naoki/github/le4-audio-kuis-main/sound/doppler_trim.wav"
  # filename = None
  isPlaying = False
  play_pos = None
  duration = None
  thread_audio = None
  wf = None   # wave.Wave_read object

  top_color = "#a5a5a5"
  left_color = "#575757"
  right_color = "#2e2e2e"

  def __init__(self, master=None):

    # ----- Root frame -----
    super().__init__(master, width=1200, height=800)
    self["bg"]="black"
    # master.attributes('-alpha', 0.7)
    self.pack(expand=True, fill="both")

    # ----- Children -----
    self.create_menubar()
    self.create_frames()
    self.create_widgets()

  
  def create_menubar(self):
    
    menubar = tk.Menu(self)
    menu_file = tk.Menu(menubar)
    menu_view = tk.Menu(menubar)
    menu_edit = tk.Menu(menubar)
    menubar.add_cascade(label="ファイル", menu=menu_file)
    menubar.add_cascade(label="編集", menu=menu_edit)
    menubar.add_cascade(label="表示", menu=menu_view)
    
    # 'file'
    menu_file.add_command(label="開く...", command=self._menu_file_open_click, accelerator="Cmd+o")
    menu_file.add_command(label="名前をつけて保存", accelerator="Cmd+S")

    # 'edit'
    menu_edit.add_command(label="元に戻す", accelerator="Cmd+Z")

    # 'view'
    menu_view.add_command(label="全画面表示", command=self._menu_view_fullscreen, accelerator="Cmd+Ctrl+F")

    self.master.config(menu=menubar)


  def create_frames(self):

    self.frame_top = tk.Frame(
      self,
      bd=2,
      relief="raised",
      bg=self.top_color,
    )
    self.frame_left = tk.Frame(
      self,
      bd=2,
      relief="raised",
      bg=self.left_color
    )
    self.frame_right = tk.Frame(
      self,
      bd=2,
      relief="raised",
      bg=self.right_color,
      width=600,
      height=400
    )

    self.frame_top.pack(side="top", anchor="n", expand=False, fill="x")
    self.frame_left.pack(side="left", anchor="n", expand=False, fill="both")
    self.frame_right.pack(side="right", anchor="n", expand=True, fill="both")


  def create_widgets(self):

    # destroy current objects in each frame
    frames = [obj for obj in self.winfo_children() if type(obj)==tk.Frame]  # list of frames
    for frame in frames:
      children = frame.winfo_children()
      for obj in children:
        obj.destroy()

    self.isPlaying = False
    self.play_pos = None
    self.duration = None
    self.thread_audio = None
      
    # ----- TOP frame -----
    button_play = tk.Button(
      self.frame_top,
      text="Play",
      highlightbackground=self.top_color,
      fg="#b93e32",
      command=self._press_button_play
    )
    button_play.pack()

    # ----- LEFT frame -----
    if (self.filename is not None) and (self.filename != ""):
      basename = os.path.basename(self.filename)
    else:
      basename = "(ファイル未選択)"

    label_filename = tk.Label(
      self.frame_left,
      text=basename,
      bg=self.left_color,
      fg="white"
    )
    label_filename.pack(side="left", anchor="center")

    # ----- RIGHT frame -----
    if self.filename is not None:
      spectrogram, melody, speech, preference = process_data(self.filename)
      self.duration = preference[3]
      self._create_plt_canvas(spectrogram, melody, self.duration)

      self.wf = wave.open(self.filename, 'rb')  # wf : Wave_read object


  def _press_button_play(self):

    if not self.isPlaying:
      self.isPlaying = True
      self.thread_audio = threading.Thread(target=self._play_audio)
      self.thread_audio.start()

    else:
      self.isPlaying = False
      self.thread_audio.join()


  def _play_audio(self):
    
    chunk = 1024

    try:
      self.wf.setpos(self.play_pos)
    except:
      self.play_pos = 0
      self.wf.rewind()

    p = pyaudio.PyAudio()

    stream = p.open(
      format = p.get_format_from_width(self.wf.getsampwidth()),
      channels = self.wf.getnchannels(),
      rate = self.wf.getframerate(),
      output = True
    )

    # while data != '' and self.isPlaying:
    while self.isPlaying and self.play_pos < self.wf.getnframes():  # isPlaying to stop playing

      play_time = self.duration * self.play_pos/self.wf.getnframes()

      # play music
      data = self.wf.readframes(chunk)
      stream.write(data)  # produce soound

      # update play_pos
      self.play_pos += chunk

    self.isPlaying = False
    stream.stop_stream()
    stream.close()
    p.terminate()


  def _create_plt_canvas(self, spectrogram, melody, duration):

    # Draw spectrogram & Melody
    fig = plt.figure()
    canvas = FigureCanvasTkAgg(fig, master=self.frame_right)	# masterに対象とするframeを指定

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

    canvas.get_tk_widget().pack(expand=True, fill="both")
    canvas.get_tk_widget().configure(width=720, height=700)

    popup_menu = tk.Menu(master=canvas.get_tk_widget())
    popup_menu.add_command(label="Tremolo")
    popup_menu.add_command(label="Voice Change")
    popup_menu.add_command(label="Vibrato")
    canvas.get_tk_widget().bind(
      "<Button-2>",
      lambda e : popup_menu.post(e.x_root, e.y_root)
    )


  def _menu_file_open_click(self):

    self.filename = tkinter.filedialog.askopenfilename(
      title='Choose .wav file',
      filetypes=[("wave file", ".wav")],
      initialdir="./"
    )
    print(self.filename)
    self.create_widgets()


  def _menu_view_fullscreen(self):

    current = self.master.attributes('-fullscreen')
    self.master.attributes('-fullscreen', not current)
    

# ----- main -----
if __name__ == '__main__':

  root = tk.Tk()
  root.title("My GarageBand")
  # root.attributes('-alpha', 0.5)
  app = Application(master=root)
  app.mainloop()