import tkinter as tk

class Application(tk.Frame):
  def __init__(self, master = None):
    super().__init__(master)

    self.master.title("Main")       # ウィンドウタイトル
    self.master.geometry("300x200") # ウィンドウサイズ(幅x高さ)

    # ボタンの作成
    btn_modeless = tk.Button(
      self.master, 
      text = "Modeless dialog",   # ボタンの表示名
      command = self.create_modeless_dialog    # クリックされたときに呼ばれるメソッド
      )
    btn_modeless.pack()

    btn_modal = tk.Button(
      self.master, 
      text = "Modal dialog",      # ボタンの表示名
      command = self.create_modal_dialog    # クリックされたときに呼ばれるメソッド
      )
    btn_modal.pack()

  def create_modeless_dialog(self):
    '''モードレスダイアログボックスの作成'''
    dlg_modeless = tk.Toplevel(self)
    dlg_modeless.title("Modeless Dialog")   # ウィンドウタイトル
    dlg_modeless.geometry("300x200")        # ウィンドウサイズ(幅x高さ)

  def create_modal_dialog(self):
    '''モーダルダイアログボックスの作成'''
    dlg_modal = tk.Toplevel(self)
    dlg_modal.title("Modal Dialog") # ウィンドウタイトル
    dlg_modal.geometry("300x200")   # ウィンドウサイズ(幅x高さ)

    # モーダルにする設定
    dlg_modal.grab_set()        # モーダルにする
    dlg_modal.focus_set()       # フォーカスを新しいウィンドウをへ移す
    dlg_modal.transient(self.master)   # タスクバーに表示しない

    # ダイアログが閉じられるまで待つ
    app.wait_window(dlg_modal)  
    print("ダイアログが閉じられた")

if __name__ == "__main__":
  root = tk.Tk()
  app = Application(master = root)
  app.mainloop()