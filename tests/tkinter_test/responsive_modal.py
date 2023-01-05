from tkinter import *
import tkinter.ttk as ttk

class ModalDialogSampleApp(ttk.Frame):

    def __init__(self, app):
        super().__init__(app)
        self.pack()
        self.param = StringVar()
        label = ttk.Label(self,text="input param")
        label.pack(side="left")
        entry = ttk.Entry(self,textvariable=self.param)
        entry.pack(side="left")
        button = ttk.Button(self,text="open",command = self.openDialog )
        button.pack(side="left")

    #パラメータを入力するモーダルダイアログを開く
    def openDialog(self):

        self.dialog = Toplevel(self)
        self.dialog.title("modal dialog")
        self.dialog.geometry("300x300")
        # modalに
        self.dialog.grab_set()
        self.paramdialog = StringVar()
        entry = ttk.Entry(self.dialog,textvariable=self.paramdialog)
        entry.pack()
        closeButton = Button(self.dialog, text="close", command=self.closeDialog)
        closeButton.pack()

    # closeする前にダイアログに入力された値を反映する
    def closeDialog(self):
        self.param.set(self.paramdialog.get())
        self.dialog.destroy()



if __name__ == '__main__':
    #Tkインスタンスを作成し、app変数に格納する
    app  = Tk()
    #縦幅400横幅300に画面サイズを変更します。
    app.geometry("400x300")
    #タイトルを指定
    app.title("Modal Dialog Sample Program")
    # #フレームを作成する
    frame =  ModalDialogSampleApp(app)
    # 格納したTkインスタンスのmainloopで画面を起こす
    app.mainloop()