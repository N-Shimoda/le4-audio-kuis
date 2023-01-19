import tkinter as tk
import tkinter.ttk as ttk

class RightFrame(tk.Frame):

  info_frame = None
  button_frame = None

  def __init__(self, master=None):

    # ----- Root of left frame -----
    super().__init__(master)
    self.pack(fill="y")

    # ----- Children -----
    self.create_frames()
    self.create_labels()
    self.create_buttons()


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

    self.info_frame.pack(expand=True, anchor="s")
    self.button_frame.pack(expand=True, anchor="n")


  def create_labels(self):

    score_label = ttk.Label(
      master=self.info_frame,
      text="96.00",
      font=("Helvetica", "32"),
      relief="raised"
    )
    score_label.pack()

    calory_label = ttk.Label(
      master=self.info_frame,
      text="54.0 kcal",
      font=("Helvetica", "32"),
      relief="raised"
    )
    calory_label.pack(anchor="center")

  
  def create_buttons(self):

    play_button = ttk.Button(
      master=self.button_frame,
      text="Play",
      command=None
    )
    play_button.pack()