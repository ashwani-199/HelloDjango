from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Create your views here.
def index(request):
    url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    products = []  # List to store the name of the product
    prices = []  # List to store price of the product
    ratings = []  # List to store rating of the product
    images = []



    data = []
    for data in soup.findAll('div', class_='_2kHMtA'):
        name = data.find('div', attrs={'class': '_4rR01T'})

        price = data.find('div', attrs={'class': '_30jeq3 _1_WHN1'})

        image = data.find('div', attrs={'class': 'CXW8mj'}).find('img')['src']

        rating = data.find('div', attrs={'class': '_3LWZlK'})
        ementa = getattr(rating, 'text', None)

        specification = data.find('div', attrs={'class': 'fMghEO'})

        products.append(name.text)  # Add product name to list
        prices.append(price.text)  # Add price to list
        ratings.append(ementa)
        images.append(image)

        # for each in specification:
        #     col = each.find_all('li', attrs={'class': 'rgWa7D'})
        #     app = col[0].text
        #     os_ = col[1].text
        #     hd_ = col[2].text
        #     sound_ = col[3].text

        #     apps.append(app)  # Add supported apps specifications to list
        #     os.append(os_)  # Add operating system specifications to list
        #     hd.append(hd_)  # Add resolution specifications to list
        #     sound.append(sound_)  # Add sound specifications to list

        df = pd.DataFrame(
            {'Product_name': products,
             'Price': prices, 'Rating': ratings, 'image': images})

        json_records = df.reset_index().to_json(orient='records')
        data = json.loads(json_records)

    context = {
        'd': data
    }
    return render(request, 'home.html', context)