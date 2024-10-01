import tkinter
import configparser
from frame_myapp import *

def read_conf():
    ini_file_name = "setting.ini"
    conf = configparser.ConfigParser()
    conf.read(ini_file_name)
    # 後での追記を考えて has_opthon しておこう
    if conf.has_option("window", "width"):
        x = conf.getint("window", "width")
    else:
        x = 1920
    if conf.has_option("window", "height"):
        y = conf.getint("window", "height")
    else:
        y = 1080
    return x, y

def hoge():
    app.app_destroy()
    root.destroy()

root = tkinter.Tk()
root.title("")
x, y = read_conf()
root.geometry(str(x)+"x"+str(y))
app = FrameMyApp(root)
app.pack(fill = tkinter.BOTH)

root.protocol("WM_DELETE_WINDOW", hoge)

root.mainloop()
