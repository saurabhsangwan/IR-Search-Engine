from bs4 import BeautifulSoup
from crawler.models import TextData
import requests
from bs4.element import Comment
import re


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    elif re.match(r"[\s\r\n]+", str(element)):
        return False
    return True


def scrape_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)
    return links


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts).encode("utf-8", errors="ignore").decode("utf-8")


def scrape_info(html, url, ):
    # create_document(html, web_pages_directory + str(filecounter) + ".txt")
    text = text_from_html(html)
    td = TextData()
    td.text = text
    td.url = url
    td.save()


def scrape_link(url):
    try:
        res = requests.get(url, timeout=(3, 60), verify=False)
        return res, url
    except requests.RequestException as e:
        return
