import os
import sys
import urllib.request
import json
from PIL import Image

def resizing(size=(256,256)) :
    dir_name =  "./static/temp"
    for index, file_name in enumerate(os.listdir(dir_name)):
        try:
            file_path = os.path.join(dir_name, file_name)
            img = Image.open(file_path)

            # 이미지 비율 계산
            img_ratio = img.size[0] / float(img.size[1])
            ratio = size[0] / float(size[1])

            # 이미지 크기 조정
            if ratio > img_ratio:
                img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))), Image.BICUBIC)
                
                # Crop
                box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
                    int(round((img.size[1] + size[1]) / 2)))
                img = img.crop(box)

            elif ratio < img_ratio:
                img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
                    Image.BICUBIC)     
                box = (int(round((img.size[0] - size[0]) / 2)), 0,
                    int(round((img.size[0] + size[0]) / 2)), img.size[1])
                img = img.crop(box)

            else :
                img = img.resize((size[0], size[1]),
                    Image.BICUBIC)
 
            img.save(dir_name + "/" + file_name)

        # 이미지 파일이 깨져있는 경우
        except OSError:
            continue