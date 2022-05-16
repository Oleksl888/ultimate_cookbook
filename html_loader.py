import csv
import json
import re


def read_csv(filename):
    """This function opens csv file, reads it into a dictionary and converts in json format"""
    with open(filename) as file:
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
        row = '<tr>\n<td>' + key + '</td>\n' + '<td>' + value + '</td>\n</tr>\n'
        html_table += row
    else:
        html_table += '<table>'
    return html_table


def make_search(keyword):
    recepies = {}
    cookdb = extract_recepies(read_csv('cookbook.csv'))
    for key, value in cookdb.items():
        if keyword in key or keyword in value:
            recepies[key] = value
    return recepies


def html_request_response(received):
    page = re.findall('^\S+\s(/.*?)\s', received)
    method = re.findall('(^\S+)\s', received)
    headers = "HTTP/1.1 200 OK\r\n"
    headers += "Content-Type: text/html; charset=utf-8\r\n"
    headers += "\r\n"
    if method[0] == 'GET':
        html_body = f"<html><body>{make_html_table(extract_recepies(read_csv('cookbook.csv')))}</body></html>"
        if page[0] == '/':
            with open('pages/index.html') as file:
                response = file.read()
        else:
            with open('pages' + page[0]) as file:
                response = file.read()
        newdata = re.split('</body>', response)
        data = headers + newdata[0] + html_body + '<body>' + newdata[1] + '\r\n\r\n'
    elif method[0] == 'POST':
        posted_data = re.findall('search=(\S+)', received)
        lookup_word = posted_data[0]
        html_body = f"<html><body>{make_html_table(make_search(lookup_word))}</body></html>"
        with open('pages' + page[0]) as file:
            response = file.read()
        newdata = re.split('</body>', response)
        data = headers + newdata[0] + html_body + '<body>' + newdata[1] + '\r\n\r\n'
    return data


if __name__ == '__main__':
    read_csv('cookbook.csv')