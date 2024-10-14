from PIL import ImageGrab
from PIL import Image, ImageTk


class MyPIL():
    def __init__(self):
        pass

    # 入力
    # image : image型
    # w : int
    # h : int
    # 戻り値
    # image型
    # memo
    # アスペクト比固定
    # アンチエイリアス有効
    def resize_image(image, w, h):
        if int(h*image.size[0]/image.size[1]) > w:
            img = image.resize((w, int(w*image.size[1]/image.size[0])), Image.LANCZOS)
        else:
            # 縦を基準にアスペクト比固定 ( h' * w/h = w' ) #アンチエイリアス有効
            img = image.resize((int(h*image.size[0]/image.size[1]), h), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img
