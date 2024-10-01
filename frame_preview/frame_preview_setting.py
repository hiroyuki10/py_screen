from tkinter import messagebox
import tkinter
import shutil
import os
import re
import threading
import copy
from .frame_preview_setting_gui import FramePreviewSettingGui
from .frame_preview_param import FramePreviewParam as Param


class FramePreviewSetting(FramePreviewSettingGui):
    def __init__(self, master, _callback=None):
        super().__init__(master)

        self.green = '#80FF80'
        self.off = '#F0F0ED'

        # png -> jpg には変換しないとダメっぽい
        # ファイルサイズ以外でjpgにしたい理由もないのでpngのままでいることにする
        # https://qiita.com/miyamotok0105/items/0630c7f360c0207d8ed0
        # https://horomary.hatenablog.com/entry/2018/11/21/004642
        # self.ext = ".jpg"
        self.write_ext = ".png"

        self.button_save.bind("<Button-1>", self.event_save)

        self.button_clear.bind("<Button-1>", self.event_clear)

        self.event_clear_callback = None

        self.entry_direct.bind('<Button-3>', self.event_path_paste)

    def event_path_paste(self, event):
        self.entry_direct.delete(0, tkinter.END)
        self.entry_direct.insert(0, self.clipboard_get())

    def event_clear(self, event):
        if self.event_clear_callback:
            self.event_clear_callback(event)
        else:
            print("self.event_clear_callback is None ...")

    def event_save(self, event):
        if Param.get_source_images() == []:
            print("no images... no save image")
            #messagebox.showwarning("title", "no images... no save image")
            print("return")
            return
        output_dir = self.get_output_dir()
        print("save dir : ", output_dir)
        save_path = os.path.join(self.entry_path.get(),output_dir)
        #output_dir = "[hoge]fuga"
        if os.path.exists(save_path):
            print(save_path, " : already exist ... no save image")
            if messagebox.askyesno('警告','フォルダを上書きしていいですか？', icon='warning'):
                print("yes")
                self.delete_files()
                #self.rename_files(save_path)
                _param = copy.deepcopy(Param)
                t1 = threading.Thread(name='rename worker1', target=lambda param=_param: self.rename_files(save_path, param))
                t1.start()
                return
            else:
                print("no")
                return
            #messagebox.showwarning("title", " : already exist ... no save image")
        #messagebox.showinfo("title", "start save")
        os.mkdir(save_path)
        _images = copy.deepcopy(Param.get_source_images())
        t1 = threading.Thread(name='rename worker1', target=lambda images=_images: self._save_images(save_path, images))
        t1.start()

    def get_output_dir(self):
        if self.v_rb1.get() == 'tagname':
            return "[" + self.entry_tag.get() + "]" + self.entry_name.get()
        else:
            return self.entry_fullpath.get()

    def delete_files(self):
        print("file delete ...")
        for _list in Param.delete_list:
            print(_list[0])
            _list[1].close()
            os.remove(_list[0])

    def rename_files(self, output_dir, _param):
        print("file rename ...")
        i = 0
        #for _list in Param.source_list:
        for _list in _param.source_list:
            if _list[0] == "":
                file_name = str('%03d' % i) + ".png"
                # 閉じるよりセーブが先
                save_path = os.path.join(output_dir,file_name)
                _list[1].save(save_path)
                _list[1].close()
                # インクリメント
                i += 1
                print("Nes Image", " -> ", save_path)
                continue
            _list[1].close()
            base_name = os.path.basename(_list[0])
            name, ext = os.path.splitext(base_name)
            file_name = str('%03d' % i)
            if name == file_name:
                print(base_name, "Same file")
            else:
                rename = file_name + ext
                move_path = os.path.join(output_dir, rename)
                print(base_name, " -> ", move_path)
                shutil.move(_list[0], move_path)
            i += 1

#            _list[1].close()
#            os.remove(_list[0])

    def _save_images(self, _dir, _images):
        for i, image in enumerate(_images):
            file_name = str('%03d' % i) + self.write_ext
            save_file = os.path.join(_dir, file_name)
            _str = str(save_file) + "   " + str('%03d' % i) + "/" + str('%03d' % (len(_images)-1))
            print(_str)
            self.label_log.config(text=_str)
            image.save(save_file)
        print("end")
        self.label_log.config(text="save finished ...")

    def set_path(self, images_path):
        print(self)
        print("---set_path----------------------------")
        print(images_path)
        sp = os.sep#セパレータ
        path = images_path[:images_path.rfind(sp)]
        if images_path.rfind(sp) == -1:
            print("no path... current directory")
            self.entry_path.delete(0, tkinter.END)
            self.entry_path.insert(0, ".\\")
        else:
            self.entry_path.delete(0, tkinter.END)
            self.entry_path.insert(0, path)
        dir = images_path[images_path.rfind(sp)+1:]
        print("path : ", path)
        print("dir : ", dir)
        tmp = self.entry_fullpath.cget('state')
        self.entry_fullpath.config(state='normal')
        self.entry_fullpath.delete(0, tkinter.END)
        self.entry_fullpath.insert(0, dir)
        self.entry_fullpath.config(state=tmp)

        tag = re.search("\[(.*)\]", dir)
        if tag is None:
            tmp = self.entry_tag.cget('state')
            self.entry_tag.config(state='normal')
            self.entry_tag.delete(0, tkinter.END)
            self.entry_tag.config(state=tmp)
            self.v_rb1.set('fullpath')
            self.select_name_type()
        else:
            print("tag : ", tag.groups())
            tmp = self.entry_tag.cget('state')
            self.entry_tag.config(state='normal')
            self.entry_tag.delete(0, tkinter.END)
            self.entry_tag.insert(0, tag.groups(0))
            self.entry_tag.config(state=tmp)
            self.v_rb1.set('tagname')
            self.select_name_type()
        name = re.search("\[.*\](.*)", dir)
        if name is None:
            if tag is None:
                tmp = self.entry_name.cget('state')
                self.entry_name.config(state='normal')
                self.entry_name.delete(0, tkinter.END)
                self.entry_name.insert(0, dir)
                self.entry_name.config(state=tmp)
            else:
                tmp = self.entry_name.cget('state')
                self.entry_name.config(state='normal')
                self.entry_name.delete(0, tkinter.END)
                self.entry_name.config(state=tmp)
            self.v_rb1.set('fullpath')
            self.select_name_type()
        else:
            print("name : ", name.groups())
            tmp = self.entry_name.cget('state')
            self.entry_name.config(state='normal')
            self.entry_name.delete(0, tkinter.END)
            self.entry_name.insert(0, name.groups(0))
            self.entry_name.config(state=tmp)
            self.v_rb1.set('tagname')
            self.select_name_type()

if __name__ == '__main__' :
    import tkinter
    from PIL import Image
    if os.path.isdir("[hoge]fuga"):
        shutil.rmtree("[hoge]fuga")
    shutil.copytree("[aaa]bbb", "[hoge]fuga")
    Param.gen_source_list("[hoge]fuga")
    print("--------")
    print(Param.source_list)
    print("--------")
    print(Param.get_source_images())
    print("--------")
    print(Param.get_source_paths())
    Param.delete_source_list(1)

    _image = Image.open("000.png")
    Param.add_source_list("", _image)

    print("--------")
    print(Param.source_list)
    print("--------")
    print(Param.get_source_images())
    print("--------")
    print(Param.get_source_paths())

    root = tkinter.Tk()
    hoge = FramePreviewSetting(root)
    hoge.event_save(0)

#    path = "C:/mydata/F/python/33_screenshot_4"
#    import sys,os
#    sp = os.sep#セパレータ
#    dirpath = sys.argv[1]
#    print("FullPath :",dirpath)
#    path = dirpath[:dirpath.rfind(sp)]
#    print("path ? :",path)
#    print("dir ? :",path[path.rfind(sp)+1:])
#    print("file name Exclude :",dirpath[dirpath.rfind(sp)+1:])

