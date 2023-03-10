from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def scrape_products(request):
    # ユーザーからキーワードを取得
    keyword = request.GET.get('keyword')

    # スクレイピング対象のECサイトのURL
    # url = f'https://example.com/products?keyword={keyword}'
    url = f'https://www.mercari.com/jp/search/?keyword={keyword}'

    # スクレイピング
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    products = []
    for product_elem in soup.select('.product'):
        name = product_elem.select_one('.product-name').text.strip()
        price = product_elem.select_one('.product-price').text.strip()
        products.append({'name': name, 'price': price})

    # 商品情報をJSON形式で返す
    return Response(products)
