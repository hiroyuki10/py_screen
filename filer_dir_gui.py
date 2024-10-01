import tkinter
import pathlib

class Core:
    def __init__(self):
        self.pfile_his = []
        self.pfile = None

    def get_pfile(self, str_path):
        pfile = pathlib.Path(str_path).resolve()
        if self.pfile:
            if self.pfile != pfile:
                self.pfile_his.append(self.pfile)
            else:
                print("same directory")
        self.pfile = pfile
        self.gen_clist()
        return self.pfile
    
    def gen_clist(self):
        self.clist = list(p for p in self.pfile.iterdir() if p.is_dir())
        for d in self.clist:
            print(d)
    
    def upper_dir(self):
        pfile = self.get_pfile(self.pfile.parent)
        return pfile

    def back_dir(self):
        if self.pfile_his == []:
            return self.pfile
        # get_pfileを使うと、また履歴に追加しちゃって堂々巡りしちゃう
        self.pfile = self.pfile_his.pop().resolve()
        self.gen_clist()
        return self.pfile

class FrameFilerDir(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.core = Core()
        self.entry = tkinter.Entry(master=self)
        self.entry.pack(fill='x')
        self.button_get_dir = tkinter.Button(master=self, text = 'get dir')
        self.button_get_dir.pack(anchor=tkinter.W)
        self.button_upper_dir = tkinter.Button(master=self, text = 'upper dir')
        self.button_upper_dir.pack(anchor=tkinter.W)
        self.button_back = tkinter.Button(master=self, text = 'back dir')
        self.button_back.pack(anchor=tkinter.W)
        
        self.entry.bind("<Return>", self.event_get_dir)
        self.button_get_dir.bind("<Button-1>", self.event_get_dir)
        self.button_upper_dir.bind("<Button-1>", self.event_upper_dir)
        self.button_back.bind("<Button-1>", self.event_back)
    
    def event_get_dir(self, event):
        _str = self.core.get_pfile(self.entry.get())
        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, _str)
        
    def event_upper_dir(self, event):
        _str = self.core.upper_dir()
        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, _str)
        
    def event_back(self, event):
        _str = self.core.back_dir()
        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, _str)
    

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('')
    root.geometry("300x200")
    app = FrameFilerDir(root)
    app.pack(fill=tkinter.BOTH)
    root.mainloop()