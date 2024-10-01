import tkinter
import os
import configparser
from frame_shelf import FrameShelf
from frame_preview import FramePreview
from frame_screenshot import FrameScreenshot
from PIL import Image


class FrameMyApp(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._master = master
        self.frame_shelf = FrameShelf(master=self, _callback=None)
        self.frame_shelf.grid(row=0, column=0, sticky=tkinter.W+tkinter.N)
        self.frame_preview = FramePreview(master=self)
        self.frame_preview.grid(row=0, column=1, sticky=tkinter.W+tkinter.N)
        self.bind('<Configure>', self._self_bind_config)

        self.frame_screenshot = FrameScreenshot(master=self, _callback=self.screenshot_callback)
        self.frame_screenshot.grid(row=0, column=2, sticky=tkinter.W+tkinter.N)

        self.frame_shelf.callback = self.func

    def screenshot_callback(self):
        # print(self)
        self.frame_preview.add(self.frame_screenshot.get_save_image())

    def func(self, name):
        print("func")
        print(name)
#        image_files = os.listdir(name)
#        images = []
#        for file in image_files:
#            _name = name+"/"+file
#            print(_name)
#            image = Image.open(_name)
#            images.append(image)
#        print(images)
#        self.frame_preview.show_preview(images)
        self.frame_preview.show_preview(str(name))

    def _self_bind_config(self, event):
        w = self._master.winfo_width()
        h = self._master.winfo_height()
        self.frame_shelf.set_size(w/3, h)
        self.frame_preview.set_size(w/3, h)

    def app_destroy(self):
        pass
#        try:
#            ini_file_name = "setting.ini"
#            conf = configparser.ConfigParser()
#            conf.read(ini_file_name)
#            if conf.has_option("image_list", "dir"):
#                conf.set("image_list", "dir", self.frame_shelf.select_path)
#            with open(ini_file_name, "w", encoding="UTF-8") as f:
#                conf.write(f)
#        except:
#            print("detect app_destroy error")
