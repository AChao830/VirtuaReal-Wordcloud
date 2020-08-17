# 介绍
虚拟主播团体VirtuaReal成员的评论&amp;弹幕爬取及词云生成

# 配置环境
需要安装的库

· python

· requests

· beautifulsoup

· jieba

· pandas

· wordcloud

版本无要求，较新即可

# 使用方法
下载代码并保存到同一文件夹

在文件夹内创建data文件夹，并在其中创建origin和cleaned文件夹

在上两个文件夹内分别创建多个文件夹，文件夹名称为NAME_LIST.txt内的用户名，其中在origin内创建的文件夹内部再创建d_comments, v_comments, danmukus三个文件夹

依次运行crawl.py, clean&amp;imtigrate.py, generateWC.py即可

NAME_LIST.txt是用户名，用户UID和进度

user_dict.txt和user_stopwords.txt是用于jieba分词的自定义字典和停用词

评论和弹幕储存在data/origin文件夹内，清洗后的数据在data/cleaned文件夹内

mask文件夹用于储存生成自定形状词云所使用的蒙版，文件名字要与用户名一致

wordcloud文件夹用于储存生成的词云

蒙版和数据自己解决

# 成果展示
详细请见BiliBili专栏

