from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
import re


def handle_name(item):
    """处理商品名字"""
    shop = item.select(".p-shop  a")[0]["title"]
    try:
        print(s)
        name = re.split("\\n", s)[1]
        name = name.strip()
    except Exception:
        name = shop.strip()
    return name
def handle_price(item):
    """处理商品价格"""
    price = item.select(".p-price")[0].get_text()
    price = re.split("\\n", price)[1]
    return price
def handle_img(item):
    """处理图片"""
    try:
        price = item.select(".p-img  img")[0]["src"]
    except Exception:
        print = price = item.select(".p-img  img")[0]["data-lazy-img"]
    return price

def get_product(href):
    """获取商品信息"""
    browser.get(href)
    whait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "li.gl-item:nth-child(1)"))
    )
    browser.execute_script("""var h = document.body.scrollHeight,
            k = 0;
        var timer = setInterval(function() {
            k += 150;
            console.log(k);
            if (k > h) clearInterval(timer);
            window.scrollTo(0,k);
        }, 500);""")

    whait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "li.gl-item:nth-child(60) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)"))
        )
    html = browser.page_source
    soup = BeautifulSoup(html,"lxml")
    items = soup.select("li.gl-item")
    f = open("r.csv", "w")
    field_name = ["店铺", "商品", "价格", "图片"]
    w = csv.DictWriter(f, fieldnames=field_name)
    w.writeheader()
    for item in items:
        # print(item.select(".p-shop  span"))
        # print(item.select(".p-shop  a")[0])
        # print(item.select(".p-shop  a")[0]["title"])

        product = {
            "店铺":item.select(".p-shop  a")[0]["title"],
            "商品":handle_name(item),
            "价格":handle_price(item),
            "图片":handle_img(item),
            }
        print(product)
        w.writerow(product)
    f.close()



browser = webdriver.Firefox()
browser.get("https://www.jd.com/")
whait = WebDriverWait(browser,40)
#等待直到加载出制定标签
whait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#J_popCtn'))
    )



ele = browser.find_element_by_id("J_cate")
ActionChains(browser).move_to_element(ele).perform()
whait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "dd[clstag='h|keycount|head|category_11d07']"))
    )
html = browser.page_source
soup = BeautifulSoup(html,"lxml")
l = soup.select("dd[clstag='h|keycount|head|category_11d07'] > a:nth-child(1)")
s = str(l[0])
print(s)

a = re.search('.* href="(.*)" target="_blank".*',s)
print(a.group(1))
href = "https:" + str(a.group(1))
get_product(href)





