from django.urls import path
from .views import scrape_products

urlpatterns = [
    path("scrape_products/", scrape_products, name="scrape_products"),
]