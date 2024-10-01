import tkinter
from tkinter import ttk


class FramePreviewSettingGui(tkinter.LabelFrame):
    def __init__(self, master, _callback=None):
        super().__init__(master)
        self.label_log = tkinter.Label(master=self, text="")
        self.label_log.pack(anchor=tkinter.W)

        self.button_save = tkinter.Button(master=self, text="save")
        self.button_save.pack(anchor=tkinter.W)

        self.button_clear = tkinter.Button(master=self, text="clear")
        self.button_clear.pack(anchor=tkinter.W)

        self.label_direct = tkinter.Label(master=self, text="direct")
        self.label_direct.pack(anchor=tkinter.W)
        self.entry_direct = tkinter.Entry(master=self)
        self.entry_direct.pack(fill='x')
        self.button_load = tkinter.Button(master=self, text="load")
        self.button_load.pack(anchor=tkinter.W)

        self.label_path = tkinter.Label(master=self, text="path")
        self.label_path.pack(anchor=tkinter.W)
        self.entry_path = tkinter.Entry(master=self)
        self.entry_path.insert(0, ".\\")
        self.entry_path.pack(fill='x')

        self.rbframe = tkinter.LabelFrame(master=self)
        self.rbframe.config(text='dir name type')
        self.rbframe.pack(fill='x')
        self.v_rb1 = tkinter.StringVar()
        self.v_rb1.set('tagname')
        self.rb1 = ttk.Radiobutton(
                self.rbframe,
                text='tag/name',
                value='tagname',
                variable=self.v_rb1)
        self.rb1.config(command = lambda : self.select_name_type())
        self.rb1.pack(anchor=tkinter.W)
        self.rb2 = ttk.Radiobutton(
                self.rbframe,
                text='full path',
                value='fullpath',
                variable=self.v_rb1)
        self.rb2.config(command = lambda : self.select_name_type())
        self.rb2.pack(anchor=tkinter.W)

        self.label_tag = tkinter.Label(master=self, text="tag")
        self.label_tag.pack(anchor=tkinter.W)
        self.entry_tag = tkinter.Entry(master=self)
        self.entry_tag.insert(0, "tag")
        self.entry_tag.pack(fill='x')

        self.label_name = tkinter.Label(master=self, text="name")
        self.label_name.pack(anchor=tkinter.W)
        self.entry_name = tkinter.Entry(master=self)
        self.entry_name.insert(0, "name")
        self.entry_name.pack(fill='x')

        self.label_fullpath = tkinter.Label(master=self, text="full path")
        self.label_fullpath.pack(anchor=tkinter.W)
        self.entry_fullpath = tkinter.Entry(master=self)
        self.entry_fullpath.insert(0, "fullpath")
        self.entry_fullpath.pack(fill='x')

        self.select_name_type()

    def select_name_type(self):
        if self.v_rb1.get() == 'tagname':
            self.entry_fullpath.config(state='disable')
            self.label_fullpath.config(state='disable')
            self.label_tag.config(state='normal')
            self.entry_tag.config(state='normal')
            self.label_name.config(state='normal')
            self.entry_name.config(state='normal')
        else:
            self.entry_fullpath.config(state='normal')
            self.label_fullpath.config(state='normal')
            self.label_tag.config(state='disable')
            self.entry_tag.config(state='disable')
            self.label_name.config(state='disable')
            self.entry_name.config(state='disable')

if __name__ == '__main__' :
    root = tkinter.Tk()
    hoge = FramePreviewSettingGui(root)
    hoge.pack(fill='x')
    hoge.mainloop()

