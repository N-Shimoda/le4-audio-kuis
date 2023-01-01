"""
from https://imagingsolution.net/program/python/tkinter/menu/
"""

import tkinter as tk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()

        self.master.title("メニューの作成")       # ウィンドウタイトル
        self.master.geometry("300x150")     # ウィンドウサイズ(幅x高さ)
        
        # ------------------------------------------------
        # メニューの作成

        # メニューバーの作成
        menubar = tk.Menu(self)

        # ファイル
        menu_file = tk.Menu(menubar, tearoff = False)
        menu_file.add_command(label = "ファイルを開く",  command = self.menu_file_open_click,  accelerator="Ctrl+O")
        menu_file.add_command(label = "名前を付けて保存", command = self.menu_file_saveas_click, accelerator="Ctrl+S")
        menu_file.add_separator() # 仕切り線
        menu_file.add_command(label = "終了",            command = self.master.destroy)
        # ショートカットキーの関連付け
        menu_file.bind_all("<Control-o>", self.menu_file_open_click)
        menu_file.bind_all("<Control-s>", self.menu_file_saveas_click)

        # 表示(Checkbutton)
        menu_disp = tk.Menu(menubar, tearoff = False)
        self.disp1_value = tk.BooleanVar()
        self.disp2_value = tk.BooleanVar()
        self.disp3_value = tk.BooleanVar()
        menu_disp.add_checkbutton(label = "表示１", command = self.menu_disp1_click, variable = self.disp1_value)
        menu_disp.add_checkbutton(label = "表示２", command = self.menu_disp2_click, variable = self.disp2_value)
        menu_disp.add_checkbutton(label = "表示３", command = self.menu_disp3_click, variable = self.disp3_value)

        # 選択(Radiobutton)
        self.radio_val = tk.IntVar() # ラジオボタンの値
        menu_select = tk.Menu(menubar, tearoff = False)
        menu_select.add_radiobutton(label = "選択１", command = self.menu_select_click, variable = self.radio_val, value = 1)
        menu_select.add_radiobutton(label = "選択２", command = self.menu_select_click, variable = self.radio_val, value = 2)
        menu_select.add_radiobutton(label = "選択３", command = self.menu_select_click, variable = self.radio_val, value = 3)

        # メニューバーに各メニューを追加
        menubar.add_cascade(label="ファイル", menu = menu_file)
        menubar.add_cascade(label="表示",     menu = menu_disp)
        menubar.add_cascade(label="選択",     menu = menu_select)

        # 親ウィンドウのメニューに、作成したメニューバーを設定
        self.master.config(menu = menubar)

    def menu_file_open_click(self, event=None):
        print("「ファイルを開く」が選択された")
        filename = filedialog.askopenfilename(
            title = "ファイルを開く",
            initialdir = "./" # 自分自身のディレクトリ
            )
        print(filename)

    def menu_file_saveas_click(self, event=None):
        print("「名前を付けて保存」が選択された")

    def menu_disp1_click(self):
        print("「表示１」が選択された")
        print(f"チェック状態は{self.disp1_value.get()}")

    def menu_disp2_click(self):
        print("「表示２」が選択された")
        print(f"チェック状態は{self.disp2_value.get()}")

    def menu_disp3_click(self):
        print("「表示３」が選択された")
        print(f"チェック状態は{self.disp3_value.get()}")

    def menu_select_click(self):
        print(self.radio_val.get(), "番目のラジオボタンが選択されました。")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()