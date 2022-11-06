#coding=utf-8

from bs4 import BeautifulSoup
import requests
import random
import os, io, sys
import threading

SITE = "https://www.meitu131.com/"
IMG_DIR = "/mnt/liyunzhi/workspace/ycc"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5712.400 QQBrowser/10.2.1957.400',
    'Referer': SITE,
    'Connection': 'close'
}

def get_page_a1(url, title=None):
    print(url, flush=True)

    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    bs = BeautifulSoup(res.text, 'lxml')

    if title == None:
        album_title = bs.find('h1').text
        print(f"New Album: {album_title}", flush=True)
    else:
        album_title = title

    try:
        img_title = url.rsplit('/', 1)[1].replace("html","jpg")
    except:
        img_title = f"{random.randint(0,9999)}.jpg"

    imgs = bs.find_all('img', border='0')
    for img in imgs:
        img_url = img['src']
        ImgThread(img_url, album_title, img_title).start()
    
    # 下一页
    try:
        next_url = bs.find_all('a', text="下一页")[0]
        get_page_a1(SITE + next_url['href'], album_title)
    except:
        print("-"*16, f"{album_title} END", "-" * 16, flush=True)


class ImgThread(threading.Thread):
    def __init__(self, img_url, _album, _img_title):
        threading.Thread.__init__(self)
        self.img_url = img_url
        self.album = _album.replace(" ", "").replace("-", "")
        self.img_dir = os.path.join(IMG_DIR, "img")
        self.img_fn = _img_title

    def run(self):
        try:
            save_dir = os.path.join(self.img_dir, self.album)
            save_file = os.path.join(save_dir, self.img_fn)
            print(f"Download {self.img_url} to {save_file}", flush=True)
            os.system(f"mkdir -p {save_dir}")
            pic_data = requests.get(self.img_url, headers=headers)
            with open(save_file, 'wb+') as f:
                f.write(pic_data.content)
        except:
            pass

ycc_home_page = f"{SITE}/nvshen/9/"

def find_albums_from_hp(home_page):
    res = requests.get(home_page, headers=headers)
    res.encoding = "utf-8"
    bs = BeautifulSoup(res.text, 'lxml')
    albums_all = bs.find_all('a', target='_blank')
    albums = [album['href'] for album in albums_all if album['href'].find("meinv")>=0]
    albums_set = set(albums)


    ret = [f"{SITE}{a}index.html" for a in albums_set]

    print(len(ret))
    return ret


if __name__ == '__main__':
    #get_page_a1("https://www.meitu131.com/meinv/4989/index.html")
    all = find_albums_from_hp(ycc_home_page)
    for a in all:
        print(f"############ {all.index(a)} ###############")
        get_page_a1(a)

