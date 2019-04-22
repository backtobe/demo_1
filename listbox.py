from tkinter import *

class make_list(Listbox):
    def __init__(self,master, **kw):
        frame = Frame(master)
        frame.pack()
        self.build_main_window(frame)

        kw['selectmode'] = SINGLE
        Listbox.__init__(self, master, kw)
        master.bind('<Button-1>', self.click_button)
        master.curIndex = None

    def click_button(self, event):
        ##this block works
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print(value)
        ##this doesn't
        self.curIndex = self.nearest(event.y)
        print(self.curIndex)
        self.curIndex = event.widget.nearest(event.y)
        print(self.curIndex)

    #display the window, calls the listbox
    def build_main_window(self, frame):
        self.build_listbox(frame)

    #listbox
    def build_listbox(self, frame):
        listbox = Listbox(frame)
        for item in ["one", "two", "three", "four"]:
            listbox.insert(END, item)
        listbox.insert(END, "a list entry")
        listbox.pack()
        return

if __name__ == '__main__':
    tk = Tk()
    make_list(tk)
    tk.mainloop()