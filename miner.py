# Copyright (c) 2020 Ahafontsev Semen(risenow)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import  requests
import  re
from bs4 import BeautifulSoup
import os
import sys

URL = "https://habr.com/ru/post/"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/77.0",
           "Accept":"*/*"}

ARTICLES_FOLDER = "/articles/"

def get_page_url(pageIdx):
    return URL + str(pageIdx) + "/"

def get_html(url, params_ = None):
    r = requests.get(url, headers = HEADERS)
    return r

def get_post_soup(pageSoup):
    return pageSoup.find('div', class_="post__wrapper")

def get_article_name_soup(postSoup):
    return postSoup.find('h1', class_="post__title post__title_full")

def get_article_text_soup(postSoup):
    return postSoup.find('div', class_="post__text post__text-html post__text_v1")

#################

begin = 0
end = 0
beginEndDict = {'b': 0, 'e': 0}

for i in range(0, len(sys.argv)-1):
    if (sys.argv[i] == "-b") or (sys.argv[i] == "-e"):
        if i + 1 <= len(sys.argv) and sys.argv[i+1].isalnum() == True:
            beginEndDict[sys.argv[i][1]] = int(sys.argv[i+1])
        else:
            print("Invalid args")
            exit(1)

if (beginEndDict["e"] == 0) or (beginEndDict["b"] == 0):
    print("Invalid args")
    exit(1)

begin = min(beginEndDict["b"], beginEndDict["e"])
end = max(beginEndDict["b"], beginEndDict["e"])

articlesFolder = os.getcwd() + ARTICLES_FOLDER;

if os.path.exists(articlesFolder)==False:
    os.mkdir(articlesFolder)

for i in range(begin, end):
    html = get_html(get_page_url(i))
    if html.status_code != 200:
        continue
    pageSoup = BeautifulSoup(html.text, 'html.parser')
    postSoup = get_post_soup(pageSoup)
    articleNameSoup = get_article_name_soup(postSoup)
    articleBodySoup = get_article_text_soup(postSoup)

    fileName = articleNameSoup.text
    fileName = fileName.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+\n"})

    f = open(articlesFolder + fileName + ".txt", 'tw', encoding='utf-8')
    f.write(articleBodySoup.text)
    f.close()
    print("Loaded article with id: " + str(i))
