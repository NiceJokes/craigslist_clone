from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models
import requests


BASE_CRAIGSLIST_URL = 'https://washington.craigslist.org/search/?query={}'
BASE_IMG_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search = search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))

    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features = 'html.parser')
    post_listing = soup.find_all('li',{"class":'result-row'})

    final_posting = []
    for post in post_listing:
        post_title = post.find(class_ = 'result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_ = 'result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = "N/A"

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get("data-ids").split(",")[0].split(":")[1]
            post_image_url = BASE_IMG_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_posting.append((post_title,post_url,post_price,post_image_url))

    for_frontend = {
        'search': search,
        'final_posting':final_posting,
    }
    return render(request, 'my_app/new_search.html', for_frontend)