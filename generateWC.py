import numpy as np
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from PIL import Image
from wordcloud import ImageColorGenerator
import re


def main():
    info = read_file(r'NAME_LIST.txt')
    NAME_LIST = []
    DONE_LIST = []
    for i in info:
        NAME_LIST.append(re.sub('\ufeff', '', i[0]))
        DONE_LIST.append(i[2][0])

    for k in range(0, len(NAME_LIST)):
        name = NAME_LIST[k]
        if int(DONE_LIST[k]) != 0:
            pass
        else:
            file_name = 'data/cleaned/'+str(name)+'/word_dict.txt'
            data = read_file(file_name)
            word_dict = {}
            for i in data:
                word_dict[re.sub('\ufeff', '', i[0])] = int(i[1])

            backgroud_image = np.array(Image.open('mask/'+str(name)+'.png'))
            wc = WordCloud(font_path=r'C:\Windows\Fonts\simfang.ttf',
                           width=2000,
                           height=2000,
                           mask=backgroud_image,
                           background_color='white',
                           mode='RGBA',
                           max_words=100
                           )
            wc.generate_from_frequencies(word_dict)
            wc.recolor(color_func=ImageColorGenerator(backgroud_image))
            wc.to_file('wordcloud/'+str(name)+'.png')
            print(str(name)+'生成词云完成')
    print("done")


def read_file(name):  # name：文件名称，t：读取模式(1：一维数据，2：二维数据)
    with open(name, 'r', encoding="UTF-8") as f:
        data = f.readlines()
    info = []
    for line in data:
        tmp = line[:-1].split(',')
        info.append(tmp)
    return info


main()
