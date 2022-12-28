import tkinter as tk

# class 'Application' inherits tk.Frame
class Application(tk.Frame):

  def __init__(self, master=None):
    super().__init__(master, width=1200, height=800)
    self["bg"]="black"
    self.pack(expand=True, fill="both")

    # Frames
    self.frame_top = tk.Frame(self, bd=2, relief="raised")
    self.frame_left = tk.Frame(self, bd=2, relief="raised")
    self.frame_right = tk.Frame(self, bd=2, relief="raised")
    """
    self.frame_top.place(width=self["width"], height=10)
    self.frame_left.place(width=self["width"]//2, height=self["height"]-10)
    self.frame_right.place(width=self["width"]//2, height=self["height"]-10)
    """
    self.frame_top.pack(side="top", anchor="n", expand=True, fill="x")
    self.frame_left.pack(side="left", anchor="s", expand=True, fill="both")
    self.frame_right.pack(side="right", anchor="n", expand=True, fill="both")
    
    """
    self.frame_top.grid(column=0, row=0, columnspan=2, sticky="we")
    self.frame_left.grid(column=0, row=1)
    self.frame_right.grid(column=1, row=1)
    """

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