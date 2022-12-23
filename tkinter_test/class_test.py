import tkinter as tk

class Application(tk.Frame):

  # '__init__' 関数はコンストラクタ `Application` が呼ばれるたびに絶対に実行される。
  def __init__(self, master=None):
    super().__init__(master)
    self.pack()
    self.create_widgets()

  def create_widgets(self):
    # Text "Hello world"
    self.hi_there = tk.Button(self)
    self.hi_there["text"] = "Hello World\n(click me)"
    self.hi_there["command"] = self.say_hi
    self.hi_there.pack(side="top")

    # Button to quit app
    self.quit_button = tk.Button(self, text="QUIT", fg="red",
                          command=root.destroy)
    self.quit_button.pack(side="bottom")

    # Label2
    self.info_label = tk.Label(self)
    self.info_label["text"] = "クラスの勉強中"
    self.info_label.pack(side="top")
    

  def say_hi(self):
    print("hi there, everyone!")


##-------------------------------
if __name__ == '__main__':
  root = tk.Tk()
  app = Application(master=root)
  app.mainloop()