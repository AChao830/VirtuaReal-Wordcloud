import re
import pandas as pd
import jieba


def main():
    info = read_file(r'NAME_LIST.txt', 2)
    NAME_LIST = []
    DONE_LIST = []
    for i in info:
        NAME_LIST.append(re.sub('\ufeff', '', i[0]))
        DONE_LIST.append(i[2][0])

    jieba.load_userdict("user_dict.txt")

    for k in range(0, len(NAME_LIST)):
        name = NAME_LIST[k]
        if int(DONE_LIST[k]) != 0:
            pass
        else:
            dfile_name = 'data/origin/'+str(name)+'/dynamic_info.txt'
            afile_name = 'data/origin/'+str(name)+'/video_aid_list.txt'
            bfile_name = 'data/origin/'+str(name)+'/video_bvid_list.txt'
            aids = read_file(afile_name, 1)
            bvids = read_file(bfile_name, 1)
            dinfo = read_file(dfile_name, 2)
            dids = []
            for i in dinfo:
                dids.append(i[0])

            text_list = []
            for aid in aids:
                text_list = text_list + read_file('data/origin/'+str(name)+'/v_comments/'+str(aid)+'.txt', 1)
            for bvid in bvids:
                text_list = text_list + read_file('data/origin/' + str(name) + '/danmukus/' + str(bvid) + '.txt', 1)
            for did in dids:
                try:
                    text_list = text_list + read_file('data/origin/' + str(name) + '/d_comments/' + str(did) + '.txt', 1)
                except:
                    pass
            print('评论&弹幕数:'+str(len(text_list)))

            cleaned_text_list = []
            for text in text_list:
                tmp = re.sub(r'\[.*?\]', "", text)
                cleaned_text_list.append(tmp)

            cut = []
            k = 0
            word_dict = {}
            for text in cleaned_text_list:
                tmp = jieba.lcut(text)
                # cut = cut + tmp
                for i in tmp:
                    if i in word_dict:
                        word_dict[i] = word_dict[i] + 1
                    else:
                        word_dict[i] = 1
                progress_bar(k, len(text_list), str(name)+'数据分词')
                k = k + 1
            print('\r总词语数:'+str(len(word_dict)))

            tmp = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
            word_dict_sorted = {}
            for i in tmp:
                word_dict_sorted[i[0]] = i[1]

            # word_count = pd.Series(cut).value_counts()
            # word_dict = word_count.to_dict()

            word_dict = clean_word_dict(word_dict_sorted)

            with open('data/cleaned/'+str(name)+'/word_dict.txt', 'w', encoding="UTF8") as f:
                for key, value in word_dict.items():
                    f.write(str(key)+','+str(value)+'\n')

        print(str(name)+'清洗&分词完成')

    print('done')


def storage_file(info, name):  # info：写入内容，name：文件名称，t：写入模式(1：一维数据，2：二维数据)
    try:
        with open(name, 'w', newline='', encoding="UTF-8") as f:
            for i in info:
                if isinstance(i, list):
                    for n in i:
                        f.write(str(n))
                        f.write(',')
                    f.write('\n')
                else:
                    f.write(str(i))
                    f.write('\n')
    except:
        print(str(name)+'文件写入失败')


def read_file(name, t):  # name：文件名称，t：读取模式(1：一维数据，2：二维数据)
    with open(name, 'r', encoding="UTF-8") as f:
        data = f.readlines()
    info = []
    if t == 1:
        for i in data:
            tmp = i[:-1]
            info.append(tmp)
        return info
    elif t == 2:
        for line in data:
            tmp = line.split(',')
            info.append(tmp)
        return info
    else:
        print("读取文件"+str(name)+"失败")


def clean_word_dict(word_dict):
    stopwords = read_file('user_stopwords.txt', 1)
    for stopword in stopwords:
        try:
            del word_dict[str(stopword)]
        except:
            pass
    return word_dict


def progress_bar(k, n, content):  # 进度条，k：当前次数，n：总次数，content：名称
    if k % 5 == 0:
        print('\r{}进度：{:.2f}%.'.format(content, k * 100 / n), end="")
    if k % 5 == 1:
        print('\r{}进度：{:.2f}%..'.format(content, k * 100 / n), end="")
    if k % 5 == 2:
        print('\r{}进度：{:.2f}%...'.format(content, k * 100 / n), end="")
    if k % 5 == 3:
        print('\r{}进度：{:.2f}%....'.format(content, k * 100 / n), end="")
    if k % 5 == 4:
        print('\r{}进度：{:.2f}%.....'.format(content, k * 100 / n), end="")


main()
