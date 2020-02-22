import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

# Create your views here.

CRAIGS_BASIC_URL = 'https://nashville.craigslist.org/search/?query={}'
CRAIGS_BASIC_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, "base.html")


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = CRAIGS_BASIC_URL.format(quote_plus(search))
   # print(quote_plus(final_url))
    res = requests.get(final_url)
    data = res.text
    soup = BeautifulSoup(data, features="html.parser")

    post_listings = soup.find_all("li", {"class": 'result-row'})
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_="result-title").text
        post_url = post.find("a").get("href")

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = "N/A"

        if post.find(class_='result-image').get("data-ids"):
            post_image_id = post.find(
                class_='result-image').get("data-ids").split(",")[0].split(":")[1]
            post_image_url = CRAIGS_BASIC_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_postings.append(
            (post_title, post_url, post_price, post_image_url))

    frontend_data = {
        "search": search,
        "final_postings": final_postings
    }
    return render(request, "my_app/new_search.html", frontend_data)
