from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import pprint


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


def read_excel():
    excel_data = pandas.read_excel("wine.xlsx", usecols=["Name", "Sort", "Price", "Image"])
    return excel_data.to_dict(orient="records")


def make_env():
    env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
    )
    return env


def make_rendered_page():
    template = make_env().get_template('template.html')
    rendered_page = template.render(
    factory_age=get_factory_age(),
    wines_info=read_excel()
    )
    return rendered_page


def make_index_page():
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(make_rendered_page())


def start_server():
    server = HTTPServer(('0.0.0.0', 9000), SimpleHTTPRequestHandler)
    server.serve_forever()


def main():
    # global excel_data
    # excel_data = read_excel()
    # #pprint.pprint(excel_data)
    make_index_page()
    start_server()


if __name__ == "__main__":
    main()
