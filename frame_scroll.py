import tkinter
import os

class BaseFrame(tkinter.LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = tkinter.Canvas(master=self, bg="black")
        self.canvas.bind("<MouseWheel>",  self._on_mousewheel)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

        self.bar = tkinter.Scrollbar(master=self, orient=tkinter.VERTICAL)
        self.bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.bar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.bar.set)

        self.button_frame = tkinter.Frame(master=self.canvas)
        self.button_frame.bind("<MouseWheel>",  self._on_mousewheel)
        self.canvas.create_window(
                (0, 0),
                window=self.button_frame,
                anchor=tkinter.NW,
                width=self.canvas.cget('width')
                )
        self.buttons = []

    def set_size(self, w, h):
        self.canvas.config(width=w)
        self.canvas.config(height=h)
        self._put_button(self.buttons)
        self._resize_canvas()

    def update(self, _lists):
        self._clear_button()
        self.buttons = self._create_button(_lists, self.button_frame)
        self._put_button(self.buttons)
        self._resize_canvas()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _resize_canvas(self):
        frame_h = len(self.buttons) * 27
        if int(self.canvas.cget('height')) > frame_h:
            self.canvas.config(scrollregion=(0, 0, self.canvas.cget('width'), self.canvas.cget('height')))
        else:
            self.canvas.config(scrollregion=(0, 0, self.canvas.cget('width'), frame_h))
        self.canvas.create_window((0, 0), window=self.button_frame, anchor=tkinter.NW, width=self.canvas.cget('width'))

    def _clear_button(self):
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()

    def _create_button(self, _lists, _frame):
        buttons = []
        for _name in _lists:
            button = tkinter.Button(master=_frame)
            button.config(text=_name, anchor=tkinter.W)
            button.bind("<Button-1>", lambda event, num=len(buttons), name=_name: self._callback(event, num, name))
            button.bind("<MouseWheel>",  self._on_mousewheel)
            buttons.append(button)
        return buttons

    def _put_button(self, buttons):
        for i, button in enumerate(buttons):
            button.pack_forget()
            button.pack(fill=tkinter.X)

    def _callback(self, event, num, name):
        print(event)
        print(num)
        print(name)

class FrameScroll(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self._current_row = 0
        self.button_size = [100, 25]

    def set_size(self, w, h):
        self.canvas.config(width=w)
        self.canvas.config(height=h)
        self._put_button(self.buttons, self.canvas)
        self._resize_canvas()

    def update(self, _lists, _images=None):
        self._clear_button()
        self.buttons = self._create_button(_lists, self.button_frame, _images)
        self._put_button(self.buttons, self.canvas)
        self._resize_canvas()

    def _put_button(self, buttons, canvas):

        _row = int(int(canvas.cget('width'))/(self.button_size[0]+8))
        if _row == 0:
            _row = 1
        if self._current_row == _row:
            return
        self._current_row == _row
        for i, button in enumerate(buttons):
            button.grid_forget()
            button.grid(row=int(i/_row), column=int(i % _row))

    def _resize_canvas(self):
        #print(self)
        self.button_frame.update_idletasks()
        #print("button_frame : ", self.button_frame.winfo_width(), " , ", self.button_frame.winfo_height())
        #print("canvas       : ", self.canvas.winfo_width(), " , ", self.canvas.winfo_height())
        frame_h = self.button_frame.winfo_height()
        if int(self.canvas.cget('height')) > frame_h:
            self.canvas.config(scrollregion=(0, 0, self.canvas.cget('width'), self.canvas.cget('height')))
        else:
            self.canvas.config(scrollregion=(0, 0, self.canvas.cget('width'), frame_h+50))
        self.canvas.create_window((0, 0), window=self.button_frame, anchor=tkinter.NW, width=self.canvas.cget('width'))

    def _create_button(self, _lists, _button_frame, _images=None):
        buttons = []
        pixel = tkinter.PhotoImage(width=1, height=1)
        for i, _name in enumerate(_lists):
            button = tkinter.Button(master=_button_frame)
            button.config(text=os.path.basename(_name))
            button.config(width=self.button_size[0])
            button.config(height=self.button_size[1])
            if _images == None:
                button.config(image=pixel)
            elif _images[i]:
                button.config(image=_images[i])
            else:
                button.config(image=pixel)
            #button.config(compound='c')
            button.config(compound='top')
            button.bind("<Button-1>", lambda event, num=len(buttons), name=_name: self._callback(event, num, name))
            button.bind("<MouseWheel>",  self._on_mousewheel)
            buttons.append(button)
        return buttons



###################################################################################################
if __name__ == '__main__':

    class App(tkinter.LabelFrame):
        def __init__(self, master):
            super().__init__(master=master, bd=2)
            self._master = master
            self.frame1 = FrameScroll(self)
            self.frame2 = BaseFrame(self)
            self.frame3 = FrameScroll(self)
            self.frame1.grid(row=0, column=0)
            self.frame2.grid(row=1, column=1)
            self.frame3.grid(row=2, column=2)

            self.bind('<Configure>', self._self_bind_config)

        def _self_bind_config(self, event):
            w = self._master.winfo_width()
            h = self._master.winfo_height()
            self.frame1.set_size(int(w/3), int(h/4))
            self.frame2.set_size(int(w/4), int(h/5))
            self.frame3.set_size(int(w/5), int(h/3))

        def update(self, _list):
            self.frame1.update(_list)
            self.frame2.update(_list)
            self.frame3.update(_list)

    root = tkinter.Tk()
    root.geometry("300" + "x" + "400")
    app = App(root)
    app.pack(fill='x')
    _list = [
            "hoge0", "fuga", "piyo",
            "hoge1", "fuga", "piyo",
            "hoge2", "fuga", "piyo",
            "hoge3", "fuga", "piyo",
            "hoge4", "fuga", "piyo",
            "hoge5", "fuga", "piyo",
            "hoge6", "fuga", "piyo",
            "hoge7", "fuga", "piyo",
            "hoge8", "fuga", "piyo",
            "hoge9", "fuga", "piyo",
            "hoge10", "fuga", "piyo",
            "hoge11", "fuga", "piyo",
            "hoge12", "fuga", "piyo",
            "hoge13", "fuga", "piyo",
            ]
    app.update(_list)
    root.mainloop()
