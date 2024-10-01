import tkinter
import os
import shutil
from tkinter import messagebox
from PIL import Image
from frame_thumbnail import FrameThumbnail
from filer_dir_gui import FrameFilerDir

img_ext = [".jpg", ".png", ".webp"]

class ShelfListScroll(FrameThumbnail):
    def update_lists(self, _lists):
        images = []
        for name in _lists:
            images.append(self.get_images(name))
        print(images)
        self.update(images, _lists)

    def _bind_button(self, button, _name):
        button.bind("<Button-1>", lambda event, num=len(self.buttons), name=_name: self._callback(event, num, name))
        button.bind("<Button-3>", lambda event, num=len(self.buttons), name=_name: self._callback_2(event, num, name))
        button.bind("<MouseWheel>",  self._on_mousewheel)
        return button

    def _callback_2(self, event, num, name):
        print(event)
        print(num)
        print(name)
        if messagebox.askyesno('警告', name + '\nを削除していいですか？', icon='warning'):
            print("yes")
            shutil.rmtree(name)
        else:
            print("no")

    def get_images(self, _name):
        files = os.listdir(_name)
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in img_ext:
                _path = os.path.join(_name,file)
                print(_path)
                img = Image.open(_path)
                return img
        return None

class FrameShelfDir(FrameFilerDir):
    def __init__(self, master):
        super().__init__(master)
        self.callback = None

        self.entry.bind('<Button-3>', self.event_path_paste)

    def event_path_paste(self, event):
        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, self.clipboard_get())

    def event_get_dir(self, event):
        super().event_get_dir(event)
        self.callback()
    def event_upper_dir(self, event):
        super().event_upper_dir(event)
        self.callback()
    def event_back(self, event):
        super().event_back(event)
        self.callback()

class FrameShelf(tkinter.LabelFrame):
    def __init__(self, master, _callback=None):
        super().__init__(master)
        self.config(text="shelf")
        self.callback = _callback
        self.select_path ='.'

        self.frame_shelf_controller = self.create_controller(self)
        self.frame_shelf_controller.pack(anchor=tkinter.W, fill='x')
        self.frame_list = ShelfListScroll(self)
        self.frame_list.button_size = [300, 300]
        self.frame_list._callback = self.click
        self.frame_list.pack(anchor=tkinter.W)

    def create_controller(self, _master):
        frame = tkinter.LabelFrame(master=_master, text="")
        self.frame_shelf_dir = FrameShelfDir(frame)
        self.frame_shelf_dir.callback = self.dir_callback
        self.frame_shelf_dir.pack(anchor=tkinter.W, fill='x')
        self.flag_only_image = tkinter.BooleanVar()
        self.flag_only_image.set(True)
        self.chkbtn_only_image = tkinter.Checkbutton(master=frame, text="only image", variable=self.flag_only_image)
        self.chkbtn_only_image.config(command=lambda : self.dir_callback())
        self.chkbtn_only_image.pack(anchor=tkinter.W)
        self.flag_show_thumbnail = tkinter.BooleanVar()
        self.chkbtn_show_thumbnail = tkinter.Checkbutton(master=frame, text="show thumbnail", variable=self.flag_show_thumbnail)
        self.chkbtn_show_thumbnail.config(command=lambda : self.dir_callback())
        self.chkbtn_show_thumbnail.pack(anchor=tkinter.W)
        return frame

    def set_size(self, w, h):
        self.frame_shelf_controller.update_idletasks()
        f_cnt_h = self.frame_shelf_controller.winfo_height()
        self.frame_list.set_size(w,h-f_cnt_h)

    def click(self, event, num, name):
        if self.callback:
            print("click")
            print(event)
            print(num)
            print(name)
            self.callback(name)
        else:
            print("callback None...")
            print(event, num, name)

    def get_images(self, name_list, img_dir):
        images = []
        for image_name in name_list:
            images.append(Image.open(img_dir + "/" + image_name))
        return images

    def extract_dir_has_image(self, _lists):
        image_lists = []
        for path in _lists:
            files = os.listdir(path)
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in img_ext:
                    image_lists.append(path)
                    break
        return image_lists

    def dir_callback(self):
        if self.flag_only_image.get():
            dir_list = self.extract_dir_has_image(self.frame_shelf_dir.core.clist)
        else:
            dir_list = self.frame_shelf_dir.core.clist
        self.frame_list.update_lists(dir_list)
        #print(f'{dir_list = }')

if __name__ == '__main__' :
    root = tkinter.Tk()
    frame_image_list = FrameShelf(master=root, _callback=None)
    frame_image_list.pack()
    root.mainloop()
