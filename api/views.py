from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rest_framework.decorators import api_view
from rest_framework.response import Response
from concurrent.futures import ThreadPoolExecutor

@api_view(['GET'])
def scrape_products(request, keyword):

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_Rakuma = executor.submit(scrapeRakuma,keyword)
        future_Merucari = executor.submit(scrapeMerucari,keyword)
        future_Yahoo = executor.submit(scrapeYahoo,keyword)
        future_PayPayFleamarket = executor.submit(scrapePayPayFleamarket,keyword)

    json_Merucari = future_Merucari.result()
    json_Yahoo = future_Yahoo.result()
    json_PayPayFleamarket = future_PayPayFleamarket.result()
    json_Rakuma = future_Rakuma.result()
    json = json_Merucari + json_Yahoo + json_PayPayFleamarket + json_Rakuma

    # 商品情報をJSON形式で返す
    return Response(json)


def scrapeMerucari(keyword):

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')

    url = f"https://jp.mercari.com/search?keyword={keyword}&status=on_sale"
    driver.get(url)

    # ページがロードされるまで待機
    wait = WebDriverWait(driver, 10)  # 10秒のタイムアウト
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-testid="item-cell"]')))

    html = driver.page_source.encode("utf-8")

    # Beautifulsoupで要素取得
    soup = BeautifulSoup(html, "lxml")
    items_list = soup.find_all("li", attrs={"data-testid": "item-cell"})

    products = []
    for item in items_list:
        a_tag = item.find("a")
        thumbnail_tag = item.find("mer-item-thumbnail")

        url = "https://jp.mercari.com" + a_tag["href"]
        name = thumbnail_tag["item-name"]
        price = thumbnail_tag["price"]
        image = thumbnail_tag["src"]

        products.append({"url": url, "name": name, "price": price, "image": image})

    driver.quit()

    return products

def scrapeYahoo(keyword):

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')

    url = f"https://auctions.yahoo.co.jp/search/search?auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p={keyword}&x=0&y=0"
    driver.get(url)

    # # ページがロードされるまで待機
    wait = WebDriverWait(driver, 10)  # 10秒のタイムアウト
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[class="Product"]')))

    html = driver.page_source.encode("utf-8")

    # Beautifulsoupで要素取得
    soup = BeautifulSoup(html, "lxml")
    items_list = soup.find_all("li", attrs={"class": "Product"})

    products = []
    for item in items_list:
        
        product_tag = item.find("a")

        url = product_tag["href"]
        name = product_tag["data-auction-title"]
        price = product_tag["data-auction-price"]
        image = product_tag["data-auction-img"]

        products.append({"url": url, "name": name, "price": price, "image": image})
    
    driver.quit()

    return products

def scrapePayPayFleamarket(keyword):

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')

    url = f"https://paypayfleamarket.yahoo.co.jp/search/{keyword}?open=1"
    driver.get(url)

    # ページがロードされるまで待機
    wait = WebDriverWait(driver, 10)  # 10秒のタイムアウト
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="sc-6dae2d2e-0 jRXEcC"]')))

    html = driver.page_source.encode("utf-8")

    # Beautifulsoupで要素取得
    soup = BeautifulSoup(html, "lxml")
    items_list = soup.find_all("a", attrs={"class": "sc-6dae2d2e-0 jRXEcC"})

    products = []
    for item in items_list:
        img_tag = item.find("img", attrs={"loading": "lazy"})
        price_tag = item.find("p")

        url = item["href"]
        name = img_tag["alt"]
        price = price_tag.text
        image = img_tag["src"]

        products.append({"url": url, "name": name, "price": price, "image": image})

    driver.quit()

    return products

def scrapeRakuma(keyword):

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')

    url = f"https://fril.jp/s?query={keyword}&transaction=selling"
    driver.get(url)

    # ページがロードされるまで待機
    wait = WebDriverWait(driver, 10)  # 10秒のタイムアウト
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="item"]')))

    html = driver.page_source.encode("utf-8")

    # Beautifulsoupで要素取得
    soup = BeautifulSoup(html, "lxml")
    items_list = soup.find_all("div", attrs={"class": "item-box"})

    products = []
    for item in items_list:
        a_tag = item.find("a", attrs={"class": "link_search_image"})
        img_tag = item.find("img", attrs={"class": "img-responsive lazy"})
        price_tag = item.find("span", attrs={"itemprop": "price"})

        url = a_tag["href"]
        name = img_tag["alt"]
        price = price_tag.text
        image = img_tag["data-original"]

        products.append({"url": url, "name": name, "price": price, "image": image})

    driver.quit()

    return products