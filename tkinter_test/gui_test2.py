import tkinter

def deleteEntryValue(event):
  editBox.delete(0,tkinter.END)

root = tkinter.Tk()
root.title(u"GUI_test")
root.geometry("400x400")

# label
Static1 = tkinter.Label(
  text=u'Labels can display text',
  foreground='#ff0000',  # text color
  background='#ffaacc'   # background color
)
Static1.pack()

# text box
editBox = tkinter.Entry(width=40)
editBox.insert(tkinter.END, 'Enter your name HERE.')
editBox.pack()

# button
button = tkinter.Button(text='delete text')
button.bind("<Button-3>",deleteEntryValue)
button.pack()

tkinter.mainloop()