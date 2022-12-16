"""
https://on-green-dolphin-street.com/create-simple-music-player/
"""

import tkinter
from tkinter import *
import tkinter as tk
import glob
import random
from playsound import playsound


def ButtonPush300_00(e):
	title = entry100_00.get()
	sel = var200.get()
	MusicStart(title, sel)


def MusicStart(title, sel):
	print('MusicStart')
	lst=glob.glob(title+'\\'+'*.mp3')
	print('lst =', lst)
	while(1):
		if (sel==1):
			random.shuffle(lst)
		for tune in lst:
			print('tune =', tune)
			playsound(tune)


#--  tkinter  --

root = tkinter.Tk()
root.title('ミュージックプレーヤー')

frame_100 = Frame(root, pady=5, padx=5)
frame_200 = Frame(root, pady=5, padx=5)
frame_300 = Frame(root, pady=5, padx=5)

# ラベル
label100_00 = tkinter.Label(frame_100, text="CDタイトル ", font=("MS明朝", "14"))

#入力ボックス
entry100_00 = tkinter.Entry(frame_100, width=30, bg="white", justify='center', font=("MS明朝", "14"))
entry100_00.insert(0, "Eliane Elias")

label100_00.pack(side=tk.LEFT)
entry100_00.pack(side=tk.LEFT)
frame_100.pack(fill=tk.X, padx=2, pady=2)

var200 = tkinter.IntVar()
var200.set(0)

# ラベル
label200_00 = tkinter.Label(frame_200, text="曲順  ", font=("MS明朝", "14"))

# ラジオボタン
rdo200_00 = tkinter.Radiobutton(frame_200, value=0, variable=var200, text='ノーマル', font=("MS明朝", "14"))
rdo200_01 = tkinter.Radiobutton(frame_200, value=1, variable=var200, text='ランダム', font=("MS明朝", "14"))

label200_00.pack(side = 'left')
rdo200_00.pack(side = 'left')
rdo200_01.pack(side = 'left')
frame_200.pack(fill=tk.X, padx=2, pady=2)

#ボタン
button300_00 = tkinter.Button(frame_300, text="スタート", fg="white", bg="#0000FF", height="1", width="20", font=("MS明朝", "14"))

button300_00.pack(side=tk.LEFT)
frame_300.pack(fill=tk.X, padx=2, pady=2)

#ボタン処理
button300_00.bind("<Button-1>", ButtonPush300_00)

root.mainloop()