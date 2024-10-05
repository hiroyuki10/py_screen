import tkinter
import os
from PIL import Image
from .frame_preview_body import FramePreviewBody
from .frame_preview_setting import FramePreviewSetting
from .frame_preview_param import FramePreviewParam as Param


class FramePreview(tkinter.LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.config(text="FramePreview")
        self.setting = FramePreviewSetting(self)
        self.setting.pack(fill="x")
        self.body = FramePreviewBody(self)
        self.body.pack(fill="x")
        self.setting.event_clear_callback = self._setting_callback_clear

        self.setting.entry_direct.bind("<Return>", self.event_direct)
        self.setting.button_load.bind("<Button-1>", self.event_direct)

    def event_direct(self, event):
        path = self.setting.entry_direct.get()
        self.show_preview(path)

    def _setting_callback_clear(self, event):
        Param.clear()
        self.body._clear_button()

    def show_preview(self, image_path):
        # image_path : ディレクトリ名
        self.setting.set_path(image_path)
        Param.clear()
        Param.gen_source_list(image_path)
        # self.body.update(Param.get_source_images())
        self.body.update(Param.get_source_images())

    def add(self, image):
        # image : Image.open()
        Param.add_source_list("", image)
        self.body.add_button(image)

    def body_left_click(self, name, event, num):
        print(self)

    def set_size(self, w, h):
        self.setting.update_idletasks()
        f_setting_h = self.setting.winfo_height()
        # self.frame_list.set_size(w,h-100)
        self.body.set_size(w, h - f_setting_h)


if __name__ == "__main__":
    root = tkinter.Tk()
    hoge = FramePreview(root)
    hoge.pack()
    hoge.show_preview("[aaa]bbb")
    print(Param.source_list)

    root.mainloop()
