import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os

BASE_URL = 'https://proceedings.neurips.cc/'


# 打开网站并下载
def openAndDownload(url, title):
    str_subhtml = requests.get(url)
    soup1 = BeautifulSoup(str_subhtml.text, 'lxml')
    subdata = soup1.select('body > div.container-fluid > div > div > a:nth-child(2)')
    if len(subdata)>0:
        downloadUrl = BASE_URL + subdata[0].get('href')
        print(downloadUrl)
        getFile(downloadUrl, title)


# 下载文件
def getFile(url, title):
    title = replaceIllegalStr(title)
    filename = title + '.pdf'
    # print(filename.split('/')[-1].repalce("\t",""))
    try:
        urlretrieve(url, './iclr2021/%s' % filename.split('/')[-1].replace("\t","").replace("|",""))
        print("Sucessful to download " + title)
    except:
        pass




# 替换非法命名字符
def replaceIllegalStr(str):
    str = str.replace(':', '')
    str = str.replace('?', '')
    str = str.replace('/', '')
    str = str.replace('\\', '')
    return str


def main():
    url = 'https://proceedings.neurips.cc/paper/2021'
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    data = soup.select('body > div.container-fluid > div > ul > li > a')

    list = []
    for item in data:
        list.append([item.get_text(), item.get('href')])

    name = ['title', 'link']
    
    test = pd.DataFrame(columns=name, data=list)
    print(test)
    test.to_csv('./essayList.csv')
    # 检查是否下载过
    file_dir = os.path.join(os.getcwd(), 'iclr2021')
    downloaded_list = []
    for root, dirs, files in os.walk(file_dir):
        downloaded_list = files

    for et, el in zip(test[name[0]], test[name[1]]):
        essay_url = BASE_URL + el
        checkname = et + '.pdf'
        checkname = replaceIllegalStr(checkname)
        if (checkname in downloaded_list):
            print(checkname + ' has been downloaded! ')
        else:
            openAndDownload(essay_url, et)


if __name__ == '__main__':
    main()