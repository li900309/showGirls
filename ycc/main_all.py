#coding=utf-8

from bs4 import BeautifulSoup
import requests
import re
import os, io, sys
import threading

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5712.400 QQBrowser/10.2.1957.400',
    'Referer': 'https://www.meitulu.com/',
    'Connection': 'close'
}



def get_page_a1(url):
    print(url)
    res = requests.get(url, headers=headers)
    res.encoding="utf-8"
    bs = BeautifulSoup(res.text, 'lxml')
    imgs = bs.find_all('img', class_='content_img')
    for img in imgs:
        img_url = img['src']
        ImgThread(img_url).start()
    try:
        page = bs.find_all('a', class_='a1')[1]
        if 'https://www.meitulu.com' + page['href'] == url:
            return
        get_page_a1('https://www.meitulu.com' + page['href'])
    except:
        print("%s Error" % url)
        pass


class ImgThread(threading.Thread):
    def __init__(self, img_url, _title=""):
        threading.Thread.__init__(self)
        self.img_url = img_url
        self.title = _title

    def run(self):
        path = '/' + self.img_url[self.img_url.rfind('/img') + 5:].replace('/', '_')  # /14068_1.jpg
        if not os.path.exists('imgs' + path):
            res_pic = requests.get(self.img_url, headers=headers)
            print(path)
            with open('imgs' + path, 'wb+') as file:
                file.write(res_pic.content)
            if self.title != "":
                with open('imgs' + path + ".title", 'w+') as file:
                    file.write(self.title)

ycc_page = "https://www.meitulu.com/t/sugar-xiaotianxincc/"
if __name__ == '__main__':
    get_page_a1(ycc_page)

