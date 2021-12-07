from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import read
from typing import Collection
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
from jinja2.utils import generate_lorem_ipsum
import pandas
from pprint import pprint, pformat
import collections


def get_factory_age():
    wine_factory_founded_year = int("1920")
    current_year = datetime.datetime.now().year
    delta_year = current_year - wine_factory_founded_year
    delta_year_ends = ["год", "года", "лет"]
    year_word = ""
    if ((delta_year % 100) // 10) == 1:
        year_word = delta_year_ends[2]
    else:
        if (delta_year % 10) == 1:
            year_word = delta_year_ends[0]
        elif 2 <= (delta_year % 10) <= 4:
            year_word = delta_year_ends[1]
        else:
            year_word = delta_year_ends[2]
    return str(delta_year) + ' ' + year_word


def get_info_from_excel():
    excel_data = pandas.read_excel(
        io="example_wine_database.xlsx",
        na_values=" ",
        keep_default_na=False)
    excel_data_upd = excel_data.to_dict("records")
    wine_info_keys = []
    for item in excel_data_upd:
            wine_info_keys.append(item["Категория"])
    wine_info_keys = list(collections.Counter(wine_info_keys))
    wine_info = collections.defaultdict(list)
    for i in wine_info_keys:
        for item in excel_data_upd:
            if item["Категория"] == i:
                wine_info[i].append(item)
    return wine_info


def make_env():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']))
    return env


def make_rendered_page():
    template = make_env().get_template('template.html')
    rendered_page = template.render(
        factory_age=get_factory_age(),
        wines_info=get_info_from_excel(),
        wines_info_keys=sorted(get_info_from_excel().keys()))
    return rendered_page


def make_index_page():
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(make_rendered_page())


def start_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def main():
    make_index_page()
    start_server()


if __name__ == "__main__":
    main()
