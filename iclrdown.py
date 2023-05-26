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
        urlretrieve(url, './iclr2023/%s' % filename.split('/')[-1].replace("\t","").replace("|",""))
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
    url = 'https://api.openreview.net/notes?content.venue=ICLR+2023+poster&details=replyCount&offset=1000&limit=500&invitation=ICLR.cc%2F2023%2FConference%2F-%2FBlind_Submission'
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    data = soup.select('body>p')
    # content > dl:nth-child(2) > dd:nth-child(3n+4) > a:nth-child(1)

    list = []
    for item in data:

        ldata = item.get_text().split(",")
        print(ldata)
        iddata =[]
        titiledata=[]
        for i in ldata:
            if i.find('"id":')!=-1:
                iddata.append(i.split(":")[-1].strip('"'))
            if i.find('"title":')!=-1:
                titiledata.append(i.split(":")[-1].strip('"'))
    # print(len(iddata))
    # print(titiledata)
    for i in range(len(iddata)):
        list.append((["https://openreview.net/pdf?id="+iddata[i],titiledata[i]]))
         # list.append([item.get("href").split("/")[-1], item.get('href')])
    print(list)

    name = ['title', 'link']
    test = pd.DataFrame(columns=name, data=list)
    print(test)
    test.to_csv('./essayList.csv')
    # 检查是否下载过
    file_dir = os.path.join(os.getcwd(), 'iclr2023')
    downloaded_list = []
    for root, dirs, files in os.walk(file_dir):
        downloaded_list = files

    for et, el in zip(test[name[0]], test[name[1]]):
        checkname = el + '.pdf'
        checkname = replaceIllegalStr(checkname)
        if (checkname in downloaded_list):
            print(checkname + ' has been downloaded! ')
        else:

            # print(essay_url)
            openAndDownload(et, el)


if __name__ == '__main__':
    main()