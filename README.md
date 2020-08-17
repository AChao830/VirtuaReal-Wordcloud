# 介绍
虚拟主播团体VirtuaReal成员的评论&amp;弹幕爬取及词云生成

# 配置环境
需要安装的库

· requests

· beautifulsoup

· jieba

· pandas

· wordcloud

版本无要求，较新即可

# 使用方法
下载代码并保存到同一文件夹，依次运行crawl.py, clean&amp;imtigrate.py, generateWC.py即可

NAME_LIST.txt是用户名，用户UID和进度

user_dict.txt和user_stopwords.txt是用于jieba分词的自定义字典和停用词

评论和弹幕储存在data/origin文件夹内，清洗后的数据在data/cleaned文件夹内

mask文件夹用于储存生成自定形状词云所使用的蒙版，文件名字要与用户名一致

wordcloud文件夹用于储存生成的词云

数据和蒙版自己解决，我就不放在这了

# 成果展示
详细请见BiliBili专栏

