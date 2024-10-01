import tkinter
import os
import time
import configparser
import threading
from PIL import Image
from PIL import ImageTk
from frame_scroll import FrameScroll

class FrameThumbnail(FrameScroll):
    def __init__(self, master):
        super().__init__(master)
        self.updating_flag = False
        self.thread_kill_flag = False
        self.th_images = []

    def update(self, pil_images, _names = None):
        print("update")
        if self.updating_flag:
            if self.thread_kill_flag:
                print("wait")
                # メイン処理はここでループする
                # thread_updateがおわるまで待つ
                time.sleep(0.1)
                self.update(pil_images, _names)
            else:
                # thread_updateを終了させるためのスレッドを起動する
                t2 = threading.Thread(target=lambda images=pil_images, names=_names: self._assert_thread_kill_flag(images, names))
                t2.start()
                # 一回ループを抜けないと上記のsleepで無限ループに入る
                # なので、t2から帰ってくるようにする
        else:
            self._clear_button()
            self.th_images.clear()
            t1 = threading.Thread(target=lambda images=pil_images, names = _names: self.thread_update(images, names))
            t1.start()

    def _assert_thread_kill_flag(self, pil_images, _names):
        # フラグを立てて戻る
        self.thread_kill_flag = True
        self.update(pil_images, _names)

    def thread_update(self, pil_images, names = None):
        print("thread_update")
        self.updating_flag = True
        self.thread_kill_flag = False
        self.canvas.yview_moveto(0)
        if names:
            for image, name in zip(pil_images, names):
                print(image, name )
                if self.thread_kill_flag == False:
                    self.gen_button(image, name)
                    self._resize_canvas()
                else:
                    print("detect self.thread_kill_flag")
                    break
        else:
            for image in pil_images:
                print(image)
                if self.thread_kill_flag == False:
                    self.gen_button(image)
                    self._resize_canvas()
                else:
                    print("detect self.thread_kill_flag")
                    break
        self.thread_kill_flag = False
        self.updating_flag = False
        print("thread_update end")

    def gen_button(self, image, name = None):
        _row = int(int(self.canvas.cget('width'))/(self.button_size[0]+8))
        if _row == 0:
            _row = 1
        th_image = self._resize_image(image, int(self.button_size[0]), int(self.button_size[1]))
        button = tkinter.Button(master=self.button_frame)
        if name:
            # Todo:名前が長すぎると画像がどっかいっちゃうっぽい
            #      名前が1行なので、画像を中央配置すると、ボタンサイズからはみ出てしまう。
            _text = self._gen_button_text(name)
            button.config(text=_text, anchor=tkinter.W)
        button.config(width=self.button_size[0])
        button.config(height=self.button_size[1])
        button.config(image=th_image)
        button.config(compound='left')
        button = self._bind_button(button, name)
        button.grid(row=int((len(self.buttons))/_row), column=int((len(self.buttons)) % _row))
        self.th_images.append(th_image)
        self.buttons.append(button)

    def _bind_button(self, button, _name):
        button.bind("<Button-1>", lambda event, num=len(self.buttons), name=_name: self._callback(event, num, name))
        button.bind("<MouseWheel>",  self._on_mousewheel)
        return button

    def _gen_button_text(self, name):
        base_name = os.path.basename(name)
        return base_name

    def _resize_image(self, image, w, h):
        if image is None:
            print("image None...")
            return tkinter.PhotoImage(width=w, height=h)
        if int(h * image.size[0]/image.size[1]) > w:
            img = image.resize((w, int(w * image.size[1]/image.size[0])), Image.ANTIALIAS)
        else:
            # 縦を基準にアスペクト比固定 (h' * w/h=w') #アンチエイリアス有効
            img = image.resize((int(h * image.size[0]/image.size[1]), h), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return img

if __name__ == '__main__' :
    class App(tkinter.LabelFrame):
        def __init__(self, master):
            super().__init__(master=master, bd=2)
            self._master = master
            self.frame1 = FrameThumbnail(self)
            self.frame1.button_size = [100, 100]
            self.bind('<Configure>', self._self_bind_config)
            self.frame1.grid(row=0, column=0)

        def _self_bind_config(self, event):
            w = self._master.winfo_width()
            h = self._master.winfo_height()
            self.frame1.set_size(int(w-20), int(h))

        def update(self, pil_images):
            self.frame1.update(pil_images)

    root = tkinter.Tk()
    root.geometry("300" + "x" + "400")
    app = App(root)
    app.pack(fill='x')
    dir_list = []
    all_file = os.listdir("./")
    for file in all_file:
        if os.path.isdir("."+"/"+file):
            dir_list.append("." + "/" + file)
    image_lists = []
    for path in dir_list:
        files = os.listdir(path)
        for file in files:
            name, ext = os.path.splitext(file)
            if ext == ".jpg":
                image_lists.append(path)
                break
            if ext == ".png":
                image_lists.append(path)
                break
            if ext == ".webp":
                image_lists.append(path)
                break
    image_files = os.listdir("./"+image_lists[0])
    images = []
    for file in image_files:
        _name = image_lists[0]+"/"+file
        print(_name)
        image = Image.open(_name)
        images.append(image)
    print(images)
    app.update(images)
    root.mainloop()
