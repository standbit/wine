import argparse
import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_parser():
    parser = argparse.ArgumentParser(
        description="""создаст страничку веб-сайта \
        с вашими алкогольныи напитками""")
    parser.add_argument(
        "--path",
        default="./example_wine_database.xlsx",
        help="укажите путь до excel файла с данными")
    return parser


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
    return f"{winery_age} {winery_age_word}"


def get_grouped_wines():
    args = create_parser().parse_args()
    path = args.path
    wines_excel_table = pandas.read_excel(
        io=path,
        na_values=" ",
        keep_default_na=False)
    wines = wines_excel_table.to_dict("records")
    wines_keys = []
    for wine in wines:
        wines_keys.append(wine["Категория"])
    wines_keys = list(collections.Counter(wines_keys))
    final_wines = collections.defaultdict(list)
    for key in wines_keys:
        for wine in wines:
            if wine["Категория"] == key:
                final_wines[key].append(wine)
    return final_wines


def make_env():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']))
    return env


def make_rendered_page():
    template = make_env().get_template('template.html')
    factory_age = get_factory_age()
    final_wines = get_grouped_wines()
    rendered_page = template.render(
        factory_age=factory_age,
        final_wines=final_wines)
    return rendered_page


def make_index_page():
    rendered_page = make_rendered_page()
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def start_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def main():
    make_index_page()
    start_server()


if __name__ == "__main__":
    main()
