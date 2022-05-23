import csv
import re
from flickr_api_helper import *
import datetime
import json


def read_csv(filename):
    """This function opens csv file, reads it into a dictionary and converts in json format"""
    with open(filename, encoding='utf8') as file:
        cook_book_list = []
        reader = csv.DictReader(file)
        for row in reader:
            cook_book_list.append(row)
        return cook_book_list
        # cook_book_json = json.dumps(cook_book_list)
        # print(cook_book_json)
        # return cook_book_json


def extract_recepies(cookdb):
    """This function takes a list of recepies and creates a dictionary to display on website"""
    recepies = {}
    for recipe in cookdb:
        recepies[recipe['name'].capitalize()] = recipe['ingridients']
    return recepies


def make_html_table(data):
    """Function takes a dictionary as input and returns html-formatted table with data from dictionary"""
    html_table = '<table>\n'
    html_table += '<tr>\n<th>Recipe</th>\n<th>Ingridients</th>\n</tr>\n'
    for key, value in data.items():
        row = '<tr>\n<td>' + f"{make_post_link_recipe(key)}" + '</td>\n' + '<td>' + make_post_link_ingridient(value) + '</td>\n</tr>\n'
        print(row)
        html_table += row
    else:
        html_table += '</table>'
    return html_table


def make_post_link_recipe(name):
    """Creates a form with a psot method so you can pass recepi name to handler and load a recipe"""
    form = f'''<form action="/recipe_request.html" method="post" class="inline">
    <button style="background: none; border: none; text-decoration: underline; cursor: pointer; text-align:left" 
    type="submit" name="recipe" value="{name}">
      {name}</button>'''
    return form


def make_post_link_ingridient(name):
    """Creates a form with a psot method so you can pass recepi name to handler and load a recipe"""
    form = ''
    for item in name.split(','):
        form += f'''<form action="/search_result.html" method="post" class="inline">
    <button style="background: none; border: none; text-decoration: underline; cursor: pointer; text-align:left" 
    type="submit" name="search" value="{item.strip()}">
      {item.strip().capitalize()}</button>''' + ','
    else:
        form = form.rstrip(',')
    return form


def load_recipe_from_file(name):
    read_recipe = ''
    with open('recepies.txt', encoding='utf-8-sig') as file:
        for line in file:
            if line.strip().lower() == name.lower():
                while len(line) > 1:
                    line = file.readline()
                    read_recipe += line
                return read_recipe
    return 'The recipe is not found'


def make_search(keyword):
    """Looks for a value provided in database, returns a dictionary with results"""
    recepies = {}
    cookdb = extract_recepies(read_csv('cookbook.csv'))
    if '+' in keyword:
        keyword = keyword.replace('+', ' ')
    for key, value in cookdb.items():
        if keyword.lower() in key.lower() or keyword.lower() in value.lower():
            recepies[key] = value
    return recepies


def return_recepies_html(data):
    """Function takes a dictionary as input and returns html-formatted table with recepies to display on web page"""
    html_table = '<table>\n'
    for num, key in enumerate(data.keys()):
        if num == 0 or num % 5 == 0:
            html_table += '<tr>\n'
        row = '<td>' + make_post_link_recipe(key) + '</td>\n'
        html_table += row
        if num % 5 == 4 or num == len(data)-1:
            html_table += '</tr>\n'
    else:
        html_table += '</table>'
    return html_table


def return_ingridients_html(data):
    """Function takes a dictionary as input and returns html-formatted table with ingridients to display on web page"""
    html_table = '<table>\n'
    ingridients = set(item.strip() for items in data.values() for item in list(items.split(',')))
    for num, val in enumerate(sorted(ingridients)):
        if num == 0 or num % 5 == 0:
            html_table += '<tr>\n'
        row = '<td>' + make_post_link_ingridient(val) + '</td>\n'
        html_table += row
        if num % 5 == 4 or num == len(data)-1:
            html_table += '</tr>\n'
    else:
        html_table += '</table>'
    return html_table


def html_request_response(received):
    """Takes a request from the client and returns a webpage based on request type"""
    page = re.findall('^\S+\s(/.*?)\s', received)
    method = re.findall('(^\S+)\s', received)
    headers = "HTTP/1.1 200 OK\r\n"
    headers += "Content-Type: text/html; charset=utf-8\r\n"
    headers += "\r\n"
    if method[0] == 'GET':
        if page[0] == '/' or page[0] == '/index.html':
            with open('pages/index.html') as file:
                response = file.read()
            html_body = f"{make_html_table(extract_recepies(read_csv('cookbook.csv')))}</body>"
            newdata = re.split('</body>', response)
            data = headers + newdata[0] + html_body + newdata[1] + '\r\n\r\n'
            print(data)
        elif page[0] == '/recepies.html':
            with open('pages/recepies.html') as file:
                response = file.read()
            html_body = f"{return_recepies_html(extract_recepies(read_csv('cookbook.csv')))}</body>"
            newdata = re.split('</body>', response)
            data = headers + newdata[0] + html_body + newdata[1] + '\r\n\r\n'
            print(data)
        elif page[0] == '/ingridients.html':
            with open('pages/ingridients.html') as file:
                response = file.read()
            html_body = f"{return_ingridients_html(extract_recepies(read_csv('cookbook.csv')))}</body>"
            newdata = re.split('</body>', response)
            data = headers + newdata[0] + html_body + newdata[1] + '\r\n\r\n'
            print(data)
        elif page[0] == '/gallery.html':
            with open('pages/gallery.html') as file:
                response = file.read()
            html_body = f"{gallery_loader()}</body>"
            newdata = re.split('</body>', response)
            data = headers + newdata[0] + html_body + newdata[1] + '\r\n\r\n'
            print(data)
        elif page[0] == '/feedback.html':
            with open('pages/feedback.html') as file:
                response = file.read()
                print('test---------------------------')
            html_body = f"{feedback_loader()}</body>"
            print(html_body)
            newdata = re.split('</body>', response)
            data = headers + newdata[0] + html_body + newdata[1] + '\r\n\r\n'
            print(data)
        else:
            with open('pages' + page[0]) as file:
                response = file.read()
            data = headers + response + '\r\n\r\n'
            print(data)
    elif method[0] == 'POST':
        search = re.findall('search=', received)
        recipe = re.findall('recipe=', received)
        feedback = re.findall('fname=', received)
        if len(search) > 0 and search[0] == 'search=':
            posted_data = re.findall('search=(\S+)', received)
            lookup_word = posted_data[0]
            html_body = f"{make_html_table(make_search(lookup_word))}</body>"
            with open('pages' + page[0]) as file:
                response = file.read()
            newdata = re.split('</body>', response)
            data = headers + newdata[0] + html_body + newdata[1] + '\r\n\r\n'
            print(data)
        elif len(recipe) > 0 and recipe[0] == 'recipe=':
            posted_data = re.findall('recipe=(\S+)', received)
            lookup_word = posted_data[0]
            lookup_word = lookup_word.replace('+', ' ')
            html_body = f'<h1>{lookup_word}</h1>' + f'<div><img src="{check_for_image(lookup_word)}" alt="{lookup_word}"/></div>' + f'<div>{load_recipe_from_file(lookup_word)}</div>' + "</body>"
            with open('pages' + page[0]) as file:
                response = file.read()
            newdata = re.split('</body>', response)
            data = headers + newdata[0] + html_body + newdata[1] + '\r\n\r\n'
            print(data)
        elif len(feedback) > 0 and feedback[0] == 'fname=':
            posted_data = re.findall('fname=\S+', received)
            posted_data = posted_data[0].split('&')
            saved = feedback_saver(posted_data)
            html_body = f'<h2>{saved}</h2>' + "</body>"
            with open('pages' + page[0]) as file:
                response = file.read()
            newdata = re.split('</body>', response)
            data = headers + newdata[0] + html_body + newdata[1] + '\r\n\r\n'
            print(data)
    return data


def gallery_loader():
    file_list = os.listdir('./images')
    data = ''
    for file in file_list:
        data += f'<div><img src={file} alt="{file}"/></div>'
    return data


def feedback_loader():
    message = ''
    try:
        with open('feedback.txt') as db:
            for entry in db:
                entry = json.loads(entry)
                message += f"<h3>{entry['fname']} said @ {entry['msg_date']}:</h2><br>"
                msg = entry['msg']
                msg = msg.replace('+', ' ')
                message += f"<div>{msg}</div><br>"
                message += "<br>"
            print(message)
            return message
    except:
        return 'Could not open db'


def feedback_saver(message):
    try:
        with open('feedback.txt', 'a') as db:
            entry = {}
            for item in message:
                msg = item.split('=')
                entry[msg[0]] = msg[1]
            now = datetime.datetime.now()
            entry['msg_date'] = now.strftime('%d-%b-%Y, %H:%M:%S')
            print(json.dumps(entry), file=db)
    except:
        return 'Entry has not been added'
    else:
        return 'Feedback has been added, update page to see'


if __name__ == '__main__':
    html_request_response()
