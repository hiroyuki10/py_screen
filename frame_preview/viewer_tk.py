import tkinter
from PIL import Image
from PIL import ImageTk

if __name__ == "__main__":
    from frame_preview_param import FramePreviewParam as Param
else:
    from .frame_preview_param import FramePreviewParam as Param

# 画像生成するときに
# 次として生成するとき
#   -> 2pageなら+2して生成する
# 前として生成するとき
#   -> -1して生成する


class ViewerTk(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        self.w = 300
        self.h = 300
        self.geometry(f"{self.w}x{self.h}")
        self.canvas = tkinter.Canvas(
            master=self, width=self.w, height=self.h, bg="black"
        )
        self.canvas.pack()
        self.bind("<Left>", self._previous_page)
        self.bind("<Right>", self._next_page)
        self.bind("<Configure>", self._windwo_bind_config)
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Button-3>", self._popup_menu)
        self.create_popup()

    def create_popup(self):
        self.pmenu = tkinter.Menu(self, tearoff=0)
        # self.pmenu.add_command(label="hoge", command=self.hoge)
        self.show_type = tkinter.StringVar()
        self.show_type_str = ["1page", "2page"]
        self.show_type.set(self.show_type_str[0])
        for i in self.show_type_str:
            self.pmenu.add_radiobutton(
                label=i, variable=self.show_type, value=i, command=self.hoge
            )

    def hoge(self):
        print(self.show_type.get())

    def show(self, num):
        img = self._gen_img(num)
        self._update(img)

    def _popup_menu(self, event):
        self.pmenu.post(event.x_root, event.y_root)

    def _gen_img(self, num):
        # 1枚のときは分岐しない
        # 前のページ、2枚のときに表紙ならそのまま、それ以外は更に-1される
        # 上記の実装を踏まえて、ここでsel_numにいれる
        # gen_img_next,previousとかにわけないといけないか
        img = self._resize_image(Param.get_source_image(num), self.w, self.h)
        self.sel_num = num
        return img

    def _update(self, img):
        self.title(f"{self.sel_num + 1}/{Param.get_image_num()}")
        self.img = ImageTk.PhotoImage(img)
        # 画像の中心座標を設定する
        self.canvas.create_image(self.w / 2, self.h / 2, image=self.img)
        self.canvas.focus_set()

    def _resize_image(self, image, w, h):
        if int(h * image.size[0] / image.size[1]) > w:
            img = image.resize(
                (w, int(w * image.size[1] / image.size[0])), Image.LANCZOS
            )
        else:
            # 縦を基準にアスペクト比固定 ( h' * w/h = w' ) #アンチエイリアス有効
            img = image.resize(
                (int(h * image.size[0] / image.size[1]), h), Image.LANCZOS
            )
        return img

    def _previous_page(self, event):
        if self.sel_num > 1:
            self.pil_img = self._gen_img(self.sel_num - 1)
        else:
            self.pil_img = self._gen_img(Param.get_image_num() - 1)
        self._update(self.pil_img)

    def _next_page(self, event):
        if self.sel_num < Param.get_image_num() - 1:
            self.pil_img = self._gen_img(self.sel_num + 1)
        else:
            self.pil_img = self._gen_img(0)
        self._update(self.pil_img)

    def _windwo_bind_config(self, event):
        self.w = self.winfo_width()
        self.h = self.winfo_height()
        self.canvas.config(width=self.w)
        self.canvas.config(height=self.h)
        # ほんとはリサイズしたほうがいいんだろうけど、
        # このままにする
        # こだわると、元画像からリサイズしないと画像劣化する
        # ページ切り替えればいいだけのため
        self._update(self.pil_img)

    def _on_mousewheel(self, event):
        # event.delta 上が120 下が-120
        if event.delta > 0:
            self._previous_page(0)
        else:
            self._next_page(0)


if __name__ == "__main__":
    v = ViewerTk()
    v.mainloop()
