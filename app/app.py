from typing import List, Dict
import jinja2
import mysql.connector
import simplejson as json
from flask import Flask, Response
from flask import render_template

# app = Flask(__name__)
app = Flask(__name__, template_folder="templates")

templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = 'index.html'
template = templateEnv.get_template(TEMPLATE_FILE)
# outputText = template.render()


def cities_import() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'citiesData'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


@app.route('/')
def index():
    user = {'username': 'Miguel'}
    cities_data = cities_import()

    return render_template(template, title='Home', user=user, cities=cities_data)


@app.route('/api/cities')
def cities() -> str:
    js = json.dumps(cities_import())
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')
