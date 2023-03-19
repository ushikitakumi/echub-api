from django.urls import path
from .views import scrape_products

urlpatterns = [
    path("<str:keyword>/", scrape_products, name="scrape_products"),
]