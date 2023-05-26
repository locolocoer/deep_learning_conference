import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os



# 打开网站并下载
def openAndDownload(url, title):
    print(url)
    getFile(url, title)


# 下载文件
def getFile(url, title):
    title = replaceIllegalStr(title)
    filename = title + '.pdf'
    # print(filename.split('/')[-1].repalce("\t",""))
    try:
        urlretrieve(url, './iccv2019/%s' % filename.split('/')[-1].replace("\t","").replace("|",""))
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
    url = 'https://openaccess.thecvf.com/ICCV2019?day=2019-11-1'
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    data = soup.select('#content > dl:nth-child(2) > dd:nth-child(3n+4) > a:nth-child(1)')
    # content > dl:nth-child(2) > dd:nth-child(3n+4) > a:nth-child(1)
    print(data)
    list = []
    for item in data:
         list.append([item.get("href").split("/")[-1], item.get('href')])
    print(list)
    #
    name = ['title', 'link']
    test = pd.DataFrame(columns=name, data=list)
    print(test)
    test.to_csv('./essayList.csv')
    # 检查是否下载过
    file_dir = os.path.join(os.getcwd(), 'iccv2019')
    downloaded_list = []
    for root, dirs, files in os.walk(file_dir):
        downloaded_list = files

    for et, el in zip(test[name[0]], test[name[1]]):
        checkname = et + '.pdf'
        checkname = replaceIllegalStr(checkname)
        if (checkname in downloaded_list):
            print(checkname + ' has been downloaded! ')
        else:
            essay_url = 'https://openaccess.thecvf.com/'+ el
            # print(essay_url)
            openAndDownload(essay_url, et)


if __name__ == '__main__':
    main()