import tkinter as tk
import tkinter.filedialog

class Application(tk.Frame):

  left_frame = None
  right_frame = None
  
  def __init__(self, master=None):

    # ----- Root frame -----
    super().__init__(master, width=1200, height=800)
    self["bg"]="black"
    self.pack(expand=True, fill="both")

    # ----- Children -----
    self.create_menubar()
    self.create_widgets()


  def create_menubar(self):
    
    menubar = tk.Menu(self)
    menu_file = tk.Menu(menubar)
    menubar.add_cascade(label="ファイル", menu=menu_file)
    menu_file.add_command(label="開く...", command=self._menu_file_open, accelerator="Ctrl+o")


  def create_widgets(self):

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
      self.pre_filename = self.filename
      self.filename = new_filename
      self.create_widgets()


class LeftFrame(tk.Frame):
  pass


class RightFrame(tk.Frame):
  pass


# ----- main -----
if __name__ == '__main__':

  root = tk.Tk()
  root.title("JoySound")
  app = Application(master=root)
  app.mainloop()