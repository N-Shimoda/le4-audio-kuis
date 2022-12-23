import tkinter as tk

class Application(tk.Frame):

  def __init__(self, master=None):
    super().__init__(master)
    self.pack()

    # Frames
    self.frame_top = tk.Frame(self, bd=2, relief="raised")
    self.frame_left = tk.Frame(self, bd=2, relief="raised")
    self.frame_right = tk.Frame(self, bd=2, relief="raised")
    self.frame_top.pack(side="top", expand=True, fill="both")
    self.frame_left.pack(side="left", expand=True, fill="both")
    self.frame_right.pack(side="right", expand=True, fill="both")

    self.create_widgets()

  def create_widgets(self):
    # Frame TOP
    button_play = tk.Button(self.frame_top, text="Play")
    button_play.pack()

    # Frame LEFT
    label_filename = tk.Label(self.frame_left, text="hoge.wav")
    label_filename.pack()

    # Frame RIGHT
    label_right = tk.Label(
      self.frame_right,
      text = "Show waveform or chromagram HERE."
    )
    label_right.pack()


# ----- main -----
if __name__ == '__main__':
  root = tk.Tk()
  app = Application(master=root)
  app.mainloop()