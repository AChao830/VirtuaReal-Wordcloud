import requests
import selenium
from bs4 import BeautifulSoup
import re
import json
import csv
import time
import random
import jieba
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from PIL import Image

l = [1, 1, 2, 2, 4, 3, 5, 3, 4, 2, 4, 2, 3, 1, 3, 5, 2, 4, 3]

word_count = pd.Series(l).value_counts()
word_dict = word_count.to_dict()

print(word_dict)

Dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
for i in l:
    if i in Dict:
        Dict[i] = Dict[i] + 1
    else:
        Dict[i] = 1

tmp = sorted(Dict.items(), key=lambda x: x[1], reverse=True)
TMP = {}
for i in tmp:
    TMP[i[0]] = i[1]

print(TMP)
