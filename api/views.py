import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # 追加
from selenium.webdriver.support.ui import WebDriverWait  # 追加
from selenium.webdriver.support import expected_conditions as EC  # 追加
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def scrape_products(request, keyword):
    # ユーザーからキーワードを取得
    # keyword = request.GET.get('keyword')
    # keyword = "fender"

    # スクレイピング対象のECサイトのURL
    url = f"https://jp.mercari.com/search?keyword={keyword}&status=on_sale"

    # スクレイピング
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')
    driver.get(url)
    # time.sleep(1)
    wait = WebDriverWait(driver, 10)  # 10秒のタイムアウト
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-testid="item-cell"]')))
    html = driver.page_source.encode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    items_list = soup.find_all("li", attrs={"data-testid":"item-cell"})

    products = []
    for item in items_list:
        a_tag = item.find("a")
        thumbnail_tag = item.find("mer-item-thumbnail")

        url = "https://jp.mercari.com" + a_tag["href"]
        name = thumbnail_tag["item-name"]
        price = thumbnail_tag["price"]
        image = thumbnail_tag["src"]

        products.append({"url":url, "name":name, "price":price, "image":image})

    driver.quit()

    # 商品情報をJSON形式で返す
    return Response(products)
