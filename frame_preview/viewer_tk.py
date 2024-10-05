import tkinter
from PIL import Image
from PIL import ImageTk
from .frame_preview_param import FramePreviewParam as Param


class ViewerTk(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        self.image = None
        self.w = 300
        self.h = 300
        self.geometry(str(self.w) + "x" + str(self.h))
        self.canvas = tkinter.Canvas(
            master=self, width=self.w, height=self.h, bg="black"
        )
        self.canvas.pack()
        self.bind("<Left>", self._previous_page)
        self.bind("<Right>", self._next_page)
        self.bind("<Configure>", self._windwo_bind_config)
        self.bind("<MouseWheel>", self._on_mousewheel)

    def show(self, num):
        self.image_select_number = num
        self._update()

    def _update(self):
        self.title(
            str(self.image_select_number + 1)
            + "/"
            + str(len(Param.get_source_images()))
        )

        num = self.image_select_number
        if num < len(Param.get_source_images()) - 1:
            self.selected_image = self._resize_image(
                Param.get_source_image(self.image_select_number), self.w, self.h
            )
            self.selected_image2 = self._resize_image(
                Param.get_source_image(self.image_select_number + 1), self.w, self.h
            )
            self.canvas.create_image(
                self.w / 4 * 3, self.h / 2, image=self.selected_image
            )  # 画像の中心座標を設定する
            self.canvas.create_image(
                self.w / 4 * 1, self.h / 2, image=self.selected_image2
            )  # 画像の中心座標を設定する
        else:
            self.selected_image = self._resize_image(
                Param.get_source_image(self.image_select_number), self.w, self.h
            )
            self.canvas.create_image(
                self.w / 2, self.h / 2, image=self.selected_image
            )  # 画像の中心座標を設定する

        self.canvas.focus_set()

    def _resize_image(self, image, w, h):
        if int(h * image.size[0] / image.size[1]) > w:
            img = image.resize(
                (w, int(w * image.size[1] / image.size[0])), Image.ANTIALIAS
            )
        else:
            # 縦を基準にアスペクト比固定 ( h' * w/h = w' ) #アンチエイリアス有効
            img = image.resize(
                (int(h * image.size[0] / image.size[1]), h), Image.ANTIALIAS
            )
        img = ImageTk.PhotoImage(img)
        return img

    def _previous_page(self, event):
        num = self.image_select_number
        if num > 1:
            self.image_select_number -= 2
        else:
            self.image_select_number = len(Param.get_source_images()) - 2
        self._update()

    def _next_page(self, event):
        num = self.image_select_number
        if num < len(Param.get_source_images()) - 2:
            self.image_select_number += 2
        else:
            self.image_select_number = 0
        self._update()

    def _windwo_bind_config(self, event):
        self.w = self.winfo_width()
        self.h = self.winfo_height()
        self.canvas.config(width=self.w)
        self.canvas.config(height=self.h)
        self._update()

    def _on_mousewheel(self, event):
        # event.delta
        # 上が120
        # 下が-120
        if event.delta > 0:
            self._previous_page(0)
        else:
            self._next_page(0)
