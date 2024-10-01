import tkinter
import threading
import time
from PIL import Image
from PIL import ImageTk
from .frame_preview_param import FramePreviewParam as Param
from .viewer import Viewer
from frame_thumbnail import FrameThumbnail


class FramePreviewBody(FrameThumbnail):
    def __init__(self, master):
        super().__init__(master)
        self.button_size = [100, 100]
        self.viewer = Viewer()

    def _open_window(self, event, i):
        self.viewer.show_image(i)

    def _bind_button(self, button, _name):
        button.bind("<Button-1>", lambda event, num=len(self.buttons), name=_name: self._left_callback(event, num, name))
        button.bind("<Button-3>", lambda event, num=len(self.buttons), name=_name: self._right_callback(event, num, name))
        button.bind("<MouseWheel>",  self._on_mousewheel)
        return button 

    def _left_callback(self, event, num, name):
        self.viewer.show_image(num)

    def _right_callback(self, event, num, name):
        self._delete_image(event, num)

    def _delete_image(self, event, num):
        del Param.source_list[num]
        del self.th_images[num]
        for i, img in enumerate(self.th_images[num:]):
            self.buttons[i+num].config(image=img)
        self.buttons[-1].destroy()  # GUI上から消す
        self.buttons.pop()  # destroyではリストでは消えないのでここで消す

    def add_button(self, image):
        self.gen_button(image)
        self._resize_canvas()
