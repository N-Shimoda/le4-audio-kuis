import tkinter as tk
import tkinter.filedialog
import os

# class 'Application' inherits tk.Frame
class Application(tk.Frame):

  filename = "/Users/naoki/github/le4-audio-kuis-main/sound/aiueo.wav"

  def __init__(self, master=None):

    super().__init__(master, width=1200, height=800)
    self["bg"]="black"
    self.pack(expand=True, fill="both")

    # ----- Menu -----
    menubar = tk.Menu(self)
    menu_file = tk.Menu(menubar, tearoff = False)

    menubar.add_cascade(label="ファイル", menu = menu_file)
    menu_file.add_command(label="開く...", command=self.menu_file_open_click, accelerator="Cmd+O")
    menu_file.add_command(label="名前をつけて保存", accelerator="Cmd+S")

    self.master.config(menu=menubar)

    # Frames
    self.frame_top = tk.Frame(self, bd=2, relief="raised")
    self.frame_left = tk.Frame(self, bd=2, relief="raised")
    self.frame_right = tk.Frame(self, bd=2, relief="raised")

    self.frame_top.pack(side="top", anchor="n", expand=True, fill="x")
    self.frame_left.pack(side="left", anchor="s", expand=True, fill="both")
    self.frame_right.pack(side="right", anchor="n", expand=True, fill="both")

    self.create_widgets()


  def create_widgets(self):

    # destroy current objects in each frame
    frames = [obj for obj in self.winfo_children() if type(obj)==tk.Frame]  # list of frames
    for frame in frames:
      children = frame.winfo_children()
      for obj in children:
        obj.destroy()
      
    # Frame TOP
    button_play = tk.Button(self.frame_top, text="Play")
    button_play.pack()

    # Frame LEFT
    if self.filename is not None:
      basename = os.path.basename(self.filename)
    else:
      basename = "(ファイル未選択)"
    label_filename = tk.Label(self.frame_left, text=basename)
    label_filename.pack()

    # Frame RIGHT
    label_right = tk.Label(
      self.frame_right,
      text = "Show waveform or chromagram HERE."
    )
    label_right.pack()


  def menu_file_open_click(self, event=None):

    print("「ファイルを開く」が選択された")
    self.filename = tkinter.filedialog.askopenfilename(
      title='Choose .wav file',
      filetypes=[("wave file", ".wav")],
      initialdir="./"
      )
    print(self.filename)
    self.create_widgets()


# ----- main -----
if __name__ == '__main__':
  root = tk.Tk()
  app = Application(master=root)
  app.mainloop()