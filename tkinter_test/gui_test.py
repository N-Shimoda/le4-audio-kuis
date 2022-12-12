import tkinter

root = tkinter.Tk()
root.title(u"GUI_test")
root.geometry("400x300")

# label
Static1 = tkinter.Label(
  text=u'Labels can display text',
  foreground='#ff0000',  # text color
  background='#ffaacc'   # background color
)
Static1.pack()

# text box
editBox = tkinter.Entry(width=100)
editBox.insert(tkinter.END, 'Enter your name HERE.')
editBox.pack()

tkinter.mainloop()