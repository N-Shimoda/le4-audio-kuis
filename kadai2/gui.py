import tkinter as tk
import tkinter.filedialog
import matplotlib.pyplot as plt
import numpy as np
import threading
import os
import wave
import pyaudio

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.process import analyze_sound
from src.sound_effect import apply_effect


# class 'Application' inherits tk.Frame
class Application(tk.Frame):

  filename = "/Users/naoki/github/le4-audio-kuis-main/sound/doppler_trim.wav"
  # filename = None
  isPlaying = False
  play_pos = None
  duration = None
  thread_audio = None
  wf = None   # wave.Wave_read object
  pref_list = None

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

      spectrogram, melody, speech, preference = analyze_sound(self.filename)
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
      # x_array = self.x[self.play_pos : self.play_pos+chunk]
      # data = np.ndarray.tobytes(x_array)
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

    # ----- pop-up menu -----
    popup_top = tk.Menu(master=canvas.get_tk_widget())
    popup_2nd = tk.Menu(popup_top)
    popup_top.add_cascade(label="エフェクト", menu=popup_2nd)

    popup_2nd.add_command(
      label="Voice Change",
      command=(lambda: self._create_effect_preference("Voice Change"))
    )
    popup_2nd.add_command(
      label="Tremolo",
      command=(lambda: self._create_effect_preference("Tremolo"))
    )
    popup_2nd.add_command(
      label="Vibrato",
      command=(lambda: self._create_effect_preference("Vibrato"))
    )

    canvas.get_tk_widget().bind(
      "<Button-2>",
      lambda e : popup_top.post(e.x_root, e.y_root)
    )


  def _create_effect_preference(self, mode):

    # create effect window
    sub_window = EffectWindow(master=self)
    sub_window.set_mode(mode)
    sub_window.open()

    # wait for sub_window to close (parameters are updated here)
    self.wait_window(sub_window)

    # apply sound effect
    # this function generates output file (.wav) in kadai2/effect-middle
    if self.pref_list is not None:
      print("effect : {}".format(mode))
      print("preference : {}".format(self.pref_list))
      self.filename = apply_effect(self.filename, mode, self.pref_list)

    # update gui
    self.create_widgets()


  def _menu_file_open_click(self):

    # stop music player
    self.isPlaying = False

    # update filename via file dialog
    new_filename = tkinter.filedialog.askopenfilename(
      title='Choose .wav file',
      filetypes=[("wave file", ".wav")],
      initialdir="./"
    )

    # update all widgets if any file was selected
    if new_filename != "":
      self.filename = new_filename
      self.create_widgets()


  def _menu_view_fullscreen(self):

    current = self.master.attributes('-fullscreen')
    self.master.attributes('-fullscreen', not current)



class EffectWindow(tk.Toplevel):

  effect_list = ["Voice Change", "Tremolo", "Vibrato"]
  # bg_color = "gray"   # "#1b1b1b"
  mode = None
  pref_list = []
  entry_box_list = []

  def __init___(self, master):
    super().__init__(master)


  def open(self):

    # ---- init params -----
    self.entry_box_list = []
    self.pref_list = []

    # ----- window preference -----
    self.title("Effect Preference") # ウィンドウタイトル
    x_pos = self.master.winfo_screenmmwidth() // 2
    y_pos =  self.master.winfo_screenmmheight() // 2
    self.geometry("300x200+" + str(x_pos) + "+" + str(y_pos))   # ウィンドウサイズ(幅x高さ)
    # self["bg"] = self.bg_color
    self.grab_set()        # モーダルにする
    self.focus_set()       # フォーカスを新しいウィンドウをへ移す
    self.transient(self.master)   # タスクバーに表示しない

    # ----- 
    label = tk.Label(
      master=self,
      text=self.mode,
      font=("Helvetica", 24)
    )
    label.pack()

    pref_frame = self._create_pref_frame()
    pref_frame.pack()

    finish_button = tk.Button(
      master=self,
      text="完了",
      command=self._finish_button_Cb
    )
    finish_button.pack()
  

  def set_mode(self, mode):
    self.mode = mode

  
  def _finish_button_Cb(self):

    # update parameters
    for i in range(len(self.pref_list)):
      self.pref_list[i][1] = float( self.entry_box_list[i].get() )

    self.master.pref_list = self.pref_list
    self.destroy()


  def _create_pref_frame(self):
    
    # ----- default preference ----
    if self.mode == "Voice Change":
      self.pref_list.extend([['freq', 300]])

    elif self.mode == "Tremolo":
      self.pref_list.extend([['D',1], ['R',160000]])

    elif self.mode == "Vibrato":
      self.pref_list.extend([['tau_0',10], ['D',160000], ['R',80000]])

    else:
      raise ValueError("error in _create_pref_frame")

    
    # ----- create frame for exhibiting preference -----
    pref_frame = tk.Frame(master=self)

    for pref in self.pref_list:

      mini_frame = tk.Frame(pref_frame, relief="raised")
      mini_frame.pack()

      label = tk.Label(
        master=mini_frame,
        text=pref[0],
        font=("Helvetica", 16)
        # bg=self.bg_color
      )
      label.pack(side="left")

      entry = tk.Entry(
        master=mini_frame,
        # bg=self.bg_color
        # validate="all",
        # vcmd=(lambda x : isinstance(x, int), '%P')
      )
      i = self.pref_list.index(pref)
      entry.insert("end", self.pref_list[i][1])
      entry.pack(side="left")

      self.entry_box_list.append(entry)

    return pref_frame



# ----- main -----
if __name__ == '__main__':

  root = tk.Tk()
  root.title("My GarageBand")
  # root.attributes('-alpha', 0.5)
  app = Application(master=root)
  app.mainloop()