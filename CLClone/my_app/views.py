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
    print(data)
    frontend_data = {
        "search": search,
    }
    return render(request, "my_app/new_search.html", frontend_data)
