from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def get_factory_age():
    wine_factory_founded_year = int("1920")
    current_year = datetime.datetime.now().year
    delta_year = current_year - wine_factory_founded_year
    delta_year_ends = ["год", "года", "лет"]
    if ((delta_year % 100) // 10) == 1:
        return str(delta_year) + ' ' + delta_year_ends[2]
    else:
        if (delta_year % 10) == 1:
            return str(delta_year) + ' ' + delta_year_ends[0]
        elif 2 <= (delta_year % 10) <= 4:
            return str(delta_year) + ' ' + delta_year_ends[1]
        else:
            return str(delta_year) + ' ' + delta_year_ends[2]


rendered_page = template.render(factory_age=get_factory_age())

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
