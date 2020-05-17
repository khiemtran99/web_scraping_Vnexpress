from flask import Flask, render_template, request, url_for
import requests
from bs4 import BeautifulSoup
import json


app = Flask(__name__)

articles = []
titles, descriptions, images, links = [], [], [], []

def vnexpess():
    titles, descriptions, images, links = [], [], [], []

    # Crawl data
    # Get HTML
    try:
        BASE_URL = 'https://vnexpress.net'
        response = requests.get(BASE_URL)
    except Exception as err:
        print(f'ERROR: {err}')

    # Extract data
    soup = BeautifulSoup(response.text)
    articles = soup.find_all('article', class_='item-news')

    for article in articles:
        try:
            if article.find('p', class_='description'):
                descriptions.append(article.find('p', class_='description').text.strip())
            else:
                continue
            if article.find('img'):
                s = article.find('img')['src']
                images.append(s)
            else:
                images.append('NA')
            titles.append(article.find('a')['title'].strip())
            links.append(article.a['href'])
        except Exception as error:
            print(error)

    d = list(zip(titles, images, descriptions, links))

    with open('vnexpress.json', 'w') as file:
        json.dump(d, file)

def load_data(filename):
    with open(filename, 'r') as file:
        loaded_data = json.load(file)
    return loaded_data

@app.route('/')
def index():
    vnexpess()
    reloaded = load_data('vnexpress.json')
    #dantri()
    #data_dantri = load_data('dantri.json')
    
    return render_template('mainpage.html', reloaded=reloaded, titles=titles, descriptions=descriptions, images=images, links=links)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 