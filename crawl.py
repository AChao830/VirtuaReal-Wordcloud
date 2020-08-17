import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random


def main():
    info = read_file(r'NAME_LIST.txt', 2)
    NAME_LIST = []
    UUID_LIST = []
    DONE_LIST = []
    for i in info:
        NAME_LIST.append(re.sub('\ufeff', '', i[0]))
        UUID_LIST.append(i[1])
        DONE_LIST.append(i[2])

    for i in range(0, len(NAME_LIST)):

        if int(DONE_LIST[i]) == 0:

            print('\r爬取'+str(NAME_LIST[i])+'视频信息中')
            aids, bvids = get_aids_from_target(UUID_LIST[i])
            storage_file(bvids, 'data/origin/' + NAME_LIST[i] + '/video_bvid_list.txt')
            storage_file(aids, 'data/origin/' + NAME_LIST[i] + '/video_aid_list.txt')

            for k in range(len(aids)):
                content = get_comments_from_oid(aids[k], '1')
                storage_file(content[1], 'data/origin/' + NAME_LIST[i] + '/v_comments/' + str(aids[k]) + '.txt')
                danmuku = get_danmukus_from_bvid(bvids[k])
                storage_file(danmuku, 'data/origin/' + NAME_LIST[i] + '/danmukus/' + str(bvids[k]) + '.txt')
                progress_bar(k, len(aids), NAME_LIST[i]+'视频')

            print('\r爬取'+str(NAME_LIST[i])+'动态信息中')
            dinfo = get_dids_from_target(UUID_LIST[i])
            storage_file(dinfo, 'data/origin/' + NAME_LIST[i] + '/dynamic_info.txt')
            rids = []
            rtypes = []
            dids = []
            for n in dinfo:
                rids.append(n[1])
                rtypes.append(n[2])
                dids.append(n[0])

            for k in range(len(rids)):
                if rtypes[k] == 1:
                    pass
                else:
                    content = get_comments_from_oid(rids[k], rtypes[k])
                    storage_file(content[1], 'data/origin/' + NAME_LIST[i] + '/d_comments/' + str(dids[k]) + '.txt')
                    progress_bar(k, len(rids), NAME_LIST[i]+'动态')
        else:
            pass

        print(NAME_LIST[i]+'完成')

    print('DONE')


def storage_file(info, name):  # info：写入内容，name：文件名称，t：写入模式(1：一维数据，2：二维数据)
    # try:
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
    # except:
    #     print(str(name)+'文件写入失败')


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
            tmp = line[:-1].split(',')
            info.append(tmp)
        return info
    else:
        print("读取文件"+str(name)+"失败")


def get_json_from_url(url):  # 通过url获取json格式字典
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    try:
        r = requests.session()
        r.keep_alive = False
        r = requests.get(url, timeout=100, headers=headers)
        r.raise_for_status()
        jsDict = json.loads(r.text)
        time.sleep(random.random()+0.5)
        return jsDict
    except:
        time.sleep(random.random()+0.5)
        return {}


def get_html_from_url(url):  # 通过url获取html格式字符串
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    try:
        r = requests.session()
        r.keep_alive = False
        r = requests.get(url, timeout=100, headers=headers)
        r.raise_for_status()
        time.sleep(random.random() + 0.5)
        return r.text
    except:
        time.sleep(random.random() + 0.5)
        return ""


def get_soup_from_html(html):  # 对html格式内容进行BeautifulSoup解析
    soup = BeautifulSoup(html)
    return soup


def progress_bar(k, n, content):  # 进度条，k：当前次数，n：总次数，content：名称
    if k % 5 == 0:
        print('\r爬取{}进度：{:.2f}%.'.format(content, k * 100 / n), end="")
    if k % 5 == 1:
        print('\r爬取{}进度：{:.2f}%..'.format(content, k * 100 / n), end="")
    if k % 5 == 2:
        print('\r爬取{}进度：{:.2f}%...'.format(content, k * 100 / n), end="")
    if k % 5 == 3:
        print('\r爬取{}进度：{:.2f}%....'.format(content, k * 100 / n), end="")
    if k % 5 == 4:
        print('\r爬取{}进度：{:.2f}%.....'.format(content, k * 100 / n), end="")


def get_aids_from_target(uuid):  # 获取目标用户的视频av号信息
    pn = 1
    pntotal = 1
    aids = []
    bvids = []
    tries = 0
    while pn <= pntotal:
        if tries >= 5:
            break
        try:
            url = 'https://api.bilibili.com/x/space/arc/search?mid=' + str(uuid) + '&ps=30&tid=0&pn=' + str(
                pn) + '&keyword=&order=pubdate&jsonp=jsonp'
            jsDict = get_json_from_url(url)
            jsData = jsDict['data']
            pntotal = jsData['page']['count']//30+1
            jsVlist = jsData['list']['vlist']
            for i in jsVlist:
                aids.append(i['aid'])
                bvids.append(i['bvid'])
            pn = pn + 1
        except:
            tries = tries + 1
            pass
    return aids, bvids


def get_dids_from_target(uuid):  # 获取目标用户的动态id信息
    dinfo = []
    has_more = 1
    offset = 0
    tries = 0
    while has_more == 1:
        if tries >= 5:
            break
        try:
            url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=342578156&host_uid=' + str(
                uuid) + '&offset_dynamic_id=' + str(offset) + '&need_top=1'
            jsonDict = get_json_from_url(url)

            jsonData = jsonDict['data']
            has_more = jsonData['has_more']
            offset = jsonData['next_offset']

            for i in jsonData['cards']:
                did = i['desc']['dynamic_id_str']
                dtype = i['desc']['type']
                rtype = dtype_to_rtype(dtype)
                if int(rtype) == 17:
                    rid = did
                else:
                    rid = i['desc']['rid_str']
                dinfo.append([did, rid, rtype])
        except:
            tries = tries + 1
            pass

    return dinfo


def dtype_to_rtype(dtype):  # 动态type转换评论type
    if int(dtype) == 1:
        rtype = 17
    elif int(dtype) == 2:
        rtype = 11
    elif int(dtype) == 4:
        rtype = 17
    elif int(dtype) == 8:
        rtype = 1
    elif int(dtype) == 16:
        rtype = 5
    else:
        rtype = -1
    return str(rtype)


def get_comments_from_oid(aid, type):  # 获取视频或者动态评论信息，内容和发表者uuid, oid是...,type：视频是'1'，动态是'11'
    video_url = 'https://api.bilibili.com/x/v2/reply'  # 设置请求地址
    video_url_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    }
    pn = 1
    pntotal = 1
    comments = []
    uuids = []
    while pn <= pntotal:
        try:
            video_url_params = {
                'jsonp': 'jsonp',
                'pn': pn,
                'type': str(type),
                'oid': aid,
                'sort': '0',
            }
            repliesall = requests.session()
            repliesall.keep_alive = False
            jsContent = requests.get(video_url, params=video_url_params,
                                     headers=video_url_headers
                                     ).json()
            time.sleep(0.5 + random.random())
            pn = pn + 1
            pntotal = jsContent['data']['page']['count'] // jsContent['data']['page']['size'] + 1
            replies = jsContent['data']['replies']
            for reply in replies:
                comments.append(reply['content']['message'])
                uuids.append(reply['mid'])
        except:
            pn = pn + 1
    return [uuids, comments]


def get_danmukus_from_bvid(bvid):  # 获取视频弹幕信息，内容和发表者uuid
    try:
        url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + str(bvid) + '&jsonp=jsonp'
        text = requests.get(url).text
        time.sleep(0.5 + random.random())
        jsonDict = json.loads(text)
        cid = jsonDict['data'][0]['cid']

        url = 'http://api.bilibili.com/x/v1/dm/list.so?oid=' + str(cid)
        r = requests.get(url)
        time.sleep(0.5 + random.random())
        r.encoding = 'utf-8'
        text = r.text

        pattern = re.compile('<d.*?>(.*?)</d>')
        danmukus = pattern.findall(text)
    except:
        return []
    return danmukus


main()
