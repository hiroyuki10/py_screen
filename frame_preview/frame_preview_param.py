import os
from PIL import Image
from natsort import natsorted


class FramePreviewParam:
    source_list = []  # [0] : path, [1] : Image.oepn()
    delete_list = []

    def clear():
        __class__.source_list.clear()
        __class__.delete_list.clear()

    def gen_source_list(path):
        print(path)
        file_dir = os.listdir(path)
        for file in natsorted(file_dir):
            _file = os.path.join(path, file)
            if os.path.isfile(_file):
                name, ext = os.path.splitext(file)
                if ext == ".jpg":
                    __class__.source_list.append([_file, Image.open(_file)])
                if ext == ".png":
                    __class__.source_list.append([_file, Image.open(_file)])
                if ext == ".webp":
                    __class__.source_list.append([_file, Image.open(_file)])
        # self.body.update(images)

    def delete_source_list(num):
        if __class__.source_list[num][0] == "":
            __class__.source_list.pop(num)
        else:
            __class__.delete_list.append(__class__.source_list.pop(num))

    def add_source_list(_path, image):
        __class__.source_list.append([_path, image])

    def get_source_images():
        images = []
        for tmp in __class__.source_list:
            images.append(tmp[1])
        return images

    def get_source_image(num):
        if __class__.source_list[num]:
            return __class__.source_list[num][1]
        return None

    def get_source_paths():
        paths = []
        for tmp in __class__.source_list:
            paths.append(tmp[0])
        return paths

    def get_delete_paths():
        paths = []
        for tmp in __class__.delete_list:
            paths.append(tmp[0])
        return paths
