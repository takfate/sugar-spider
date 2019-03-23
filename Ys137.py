import requests
import os
import multiprocessing
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import time,random
bash_url = "https://www.ys137.com/tnb"

tags = {
    "yufang/list_124": (47, 2),
    "yongyao/list_125": (70, 2),
    "tnbzz/list_126": (61, 2),
    "yszn/list_127": (118, 2),
    "bfz/list_128": (90, 2),
    "cjwt/list_129": (133, 2),
}

urls_file_name = "article_urls.txt"




def get_spider_dir():
    now_dir = os.getcwd()
    data_dir = os.path.join(now_dir, "ys137")
    return data_dir


def get_url_file_path():
    return os.path.join(get_spider_dir(), urls_file_name)


def get_unique_file_path():
    return os.path.join(get_spider_dir(), "unique_" + urls_file_name)


def unique(c):
    if c == "url":
        file_path = get_url_file_path()
        unique_file_path = get_unique_file_path()
        with open(file_path, 'r') as o:
            x = o.readlines()
            olen = len(x)
            x = list(set(x))
            tlen = len(x)
            print("%d->%d" % (olen, tlen))
            with open(unique_file_path, 'w') as u:
                for i in x:
                    u.write(i)
    else:
        pass


def save_urls(content, file_string):
    now_dir = os.getcwd()
    data_dir = os.path.join(now_dir, "ys137")
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    file_path = os.path.join(data_dir, file_string)
    with open(file_path, 'a') as f:
        f.write(content+'\n')


def get_links_from_catalog(catalog_url):
    r = requests.get(catalog_url)
    r.encoding = 'GB2312'
    page = r.text
    soup = BeautifulSoup(page, "lxml")
    links = soup.select("a.arc-pic")
    article_urls = []
    for a in links:
        article_urls.append(a["href"])
    return article_urls


def get_all_tasks():
    for tag_url, page_range in tags.items():
        url = "%s/%s" % (bash_url, tag_url)
        start_page_number = page_range[1]
        end_page_number = page_range[0]
        for i in range(start_page_number, end_page_number + 1):
            final_url = "%s_%d.html" % (url, i)
            article_urls = get_links_from_catalog(final_url)
            print("page:%d->get %d items" % (i, len(article_urls)))
            for article_url in article_urls:
                save_urls(article_url, urls_file_name)


def get_all_article_urls():
    unique_file_path = get_unique_file_path()
    with open(unique_file_path, 'r') as f:
        urls = f.readlines()
    for i in range(0,len(urls)):
        urls[i] = urls[i][:-1]
    return urls


def get_article_dir_path():
    now_path = os.getcwd()
    dir_path = os.path.join(now_path, "ys137", "articles")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path


def get_article_file_path(file_string):
    return os.path.join(get_article_dir_path(), file_string+".txt")


def check_article_exists(file_string):
    file_path = get_article_file_path(file_string)
    return os.path.exists(file_path)


def fix_file_string(file_string):
    new_file_string = ""
    for i in file_string:
        if i not in "<>/\|:\"*?":
            new_file_string += i
    return new_file_string


def save_articles(content, file_string):
    file_string = fix_file_string(file_string)
    file_path = get_article_file_path(file_string)
    with open(file_path, "w", encoding="utf8") as f:
        f.write(content)


def get_content_and_title(article_url):
    r = requests.get(article_url)
    r.encoding = 'GB2312'
    page = r.text
    soup = BeautifulSoup(page, "lxml")
    title_node = soup.find("h1")
    content_node = soup.select("div.article-content")[0]
    return {
        "title": str(title_node.get_text()),
        "content": str(content_node)
    }


def start_spiders():
    flag = False
    article_urls = get_all_article_urls()
    for url in article_urls:
        if not flag:
            print("skip %s...." % url)
            if url == "https://www.ys137.com/tnb/1615820.html":
                flag = True
            continue
        time.sleep(1)
        while True:
            try:
                data = get_content_and_title(url)
                break
            except Exception :
                continue
        print("%s->%d->%d" % (url, len(data["content"]), len(data['title'])), end='.....')
        save_articles(data["content"], data["title"])
        print("save success!")





def test1():
    url = "https://www.ys137.com/tnb/tnbzz/list_126_60.html"
    r = requests.get(url)
    r.encoding = 'GB2312'
    page = r.text
    soup = BeautifulSoup(page, "lxml")
    links = soup.select("a.arc-pic")
    article_urls = []
    for a in links:
        article_urls.append(a["href"])
    return article_urls


def test2():
    url = "https://www.ys137.com/tnb/147048.html"
    r = requests.get(url)
    r.encoding = 'GB2312'
    page = r.text
    soup = BeautifulSoup(page, "lxml")
    title_node = soup.find("h1")
    content_node = soup.select("div.article-content")[0]
    return {
        "title": str(title_node.get_text()),
        "content": str(content_node)
    }


if __name__ == '__main__':
    # article_urls = test1()
    a = test2()
    print(a)
