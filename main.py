import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_factory_age():
    winery_founded_year = 1920
    winery_age = datetime.datetime.now().year - winery_founded_year
    winery_age_words = ["год", "года", "лет"]
    winery_age_word = ""
    if ((winery_age % 100) // 10) == 1:
        winery_age_word = winery_age_words[2]
    else:
        if (winery_age % 10) == 1:
            winery_age_word = winery_age_words[0]
        elif 2 <= (winery_age % 10) <= 4:
            winery_age_word = winery_age_words[1]
        else:
            winery_age_word = winery_age_words[2]
    return str(winery_age) + ' ' + winery_age_word


def get_sorted_wines_dict():
    wines_excel_table = pandas.read_excel(
        io="example_wine_database.xlsx",
        na_values=" ",
        keep_default_na=False)
    wines_dict = wines_excel_table.to_dict("records")
    wines_dict_keys = []
    for i in wines_dict:
        wines_dict_keys.append(i["Категория"])
    wines_dict_keys = list(collections.Counter(wines_dict_keys))
    wines_dict_sorted = collections.defaultdict(list)
    for i in wines_dict_keys:
        for x in wines_dict:
            if x["Категория"] == i:
                wines_dict_sorted[i].append(x)
    return wines_dict_sorted


def make_env():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']))
    return env


def make_rendered_page():
    template = make_env().get_template('template.html')
    rendered_page = template.render(
        factory_age=get_factory_age(),
        wines_dict=get_sorted_wines_dict(),
        wines_dict_keys=sorted(get_sorted_wines_dict().keys()))
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
