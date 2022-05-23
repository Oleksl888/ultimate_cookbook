import csv
import json
import re
import requests
import os


def flickr_request(query):
    url = 'https://api.flickr.com/services/rest/'
    params = {'api_key': '', 'text': query, \
              'privacy_filter': 1, 'license': 3, 'content_type': 1, 'format': 'json', 'per_page': 1,
              "method": "flickr.photos.search", 'nojsoncallback': 1}
    request = requests.get(url, params=params)
    return request.json()


def check_for_image(query):
    query = query.strip().lower()
    word = query.replace(' ', '_') + '.jpg'
    file_list = os.listdir('./images')
    # if word in file_list:
    #     print('Image found in database')
    #     path = os.path.join('./images', word)
    #     print(path)
    #     return path
    result = build_url(flickr_request(query), word)
    print(result)
    return result


def build_url(params, word):
    server_id = params['photos']['photo'][0]['server']
    id = params['photos']['photo'][0]['id']
    secret = params['photos']['photo'][0]['secret']
    url = f'https://live.staticflickr.com/{server_id}/{id}_{secret}.jpg'
    print('Adding image to database')
    write_image(url, word)
    return url


def write_image(url, query):
    request = requests.get(url)
    filename = os.path.join('./images', query)
    with open(filename, 'wb') as file:
        file.write(request.content)


if __name__ == '__main__':
    check_for_image('abalone with oyster sauce')
