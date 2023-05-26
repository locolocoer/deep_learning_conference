import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os

BASE_URL = 'https://www.ecva.net/'


# 打开网站并下载
def openAndDownload(url, title):
    # str_subhtml = requests.get(url)
    # soup1 = BeautifulSoup(str_subhtml.text, 'lxml')
    # subdata = soup1.select('body > div.container-fluid > div > div > a:nth-child(2)')
    # if len(subdata) > 0:
    #     downloadUrl = BASE_URL + subdata[0].get('href')
    print(url)
    getFile(url, title)


# 下载文件
def getFile(url, title):
    title = replaceIllegalStr(title)
    filename = title + '.pdf'
    # print(filename.split('/')[-1].repalce("\t",""))
    urlretrieve(url, './eccv2018/%s' % filename.split('/')[-1].replace("\t", "").replace("|", ""))
    print("Sucessful to download " + title)


# 替换非法命名字符
def replaceIllegalStr(str):
    str = str.replace(':', '')
    str = str.replace(',', '')
    str = str.replace('"', '')
    str = str.replace('?', '')
    str = str.replace('/', '')
    str = str.replace('\\', '')
    str = str.replace('\n', '')
    return str


def main():
    url = 'https://www.ecva.net/papers.php'
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    url = soup.select('div.accordion-content:nth-child(7) > div:nth-child(1) > dl:nth-child(1) > dd:nth-child(3n) > a:nth-child(1)')
    #print(url)
    titile = soup.select('div.accordion-content:nth-child(7) > div:nth-child(1) > dl:nth-child(1) > dt > a:nth-child(2)')
    #print(titile)
    list = []
    for u,t in zip(url,titile):
        list.append([replaceIllegalStr(t.get_text()), u.get('href')])
    print(list)
    name = ['title', 'link']

    test = pd.DataFrame(columns=name, data=list)
    print(test)
    test.to_csv('./essayList.csv')
    # 检查是否下载过
    file_dir = os.path.join(os.getcwd(), 'eccv2018')
    downloaded_list = []
    for root, dirs, files in os.walk(file_dir):
        downloaded_list = files
    i = 0
    length = len(test)
    for et, el in zip(test[name[0]], test[name[1]]):
        essay_url = BASE_URL + el
        checkname = et + '.pdf'
        checkname = replaceIllegalStr(checkname)
        if (checkname in downloaded_list):
            print(checkname + ' has been downloaded! ')
        else:
            openAndDownload(essay_url, et)
        print(i/length)
        i += 1

if __name__ == '__main__':
    main()