import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

# Create your views here.

CRAIGS_BASIC_URL = 'https://nashville.craigslist.org/search/?query={}'


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

        final_postings.append((post_title, post_url, post_price))

    frontend_data = {
        "search": search,
        "final_postings": final_postings
    }
    return render(request, "my_app/new_search.html", frontend_data)
