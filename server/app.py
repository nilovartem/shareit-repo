from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin
import psycopg2
import os

def db_connect():
    connection = psycopg2.connect(host='localhost',
                                database='shareit_db',
                                user=os.environ['POSTGRES_USERNAME'], 
                                password=os.environ['POSTGRES_PASSWORD'])
    return connection

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

connection = db_connect()
cursor = connection.cursor()

links = [
    {
        'id':1,
        'url':'www.yandex.ru',
        'description':'this is link to yandex'
    },
    {
        'id':2,
        'url':'wikipedia.org',
        'description':'this is link to wikipedia page'
    }
]


@app.route("/")
def home():
    return "Hello, you're home!"

#get all links
@app.route("/shareit/api/v1.0/links", methods=['GET'])
@cross_origin()
def get_links():#возвращает все возможные ссылки из БД
    cursor.execute("SELECT * FROM link;")
    columns=['id','url','page_id']
    results=[]
    for row in cursor.fetchall():
        results.append(dict(zip(columns,row)))
    return jsonify({'links': results})

#get link by id
@app.route("/shareit/api/v1.0/links/<int:link_id>", methods=['GET'])
@cross_origin()
def get_link(link_id):
    link = find_link(links, link_id)
    if link == None:
        abort(404)
    return jsonify({'link': link})

def find_link(links, link_id):
    for link in links:
        for key,value in link.items():
            if value == link_id:
                return link
    return None

@app.route("/shareit/api/v1.0/links", methods=['POST'])
@cross_origin()
def create_link():
    if request.method == 'POST':
        post_data = request.get_json()
        link = {
            'id':links[-1]['id'] + 1,
            'url':post_data['url'],
            'description':post_data['description']
        }
        print(link)
        links.append(link)
        print(links)
    else:
        abort(400)
    return jsonify({'link': link}), 201#http created
#create empty page(no db)
@app.route("/shareit/api/v1.0/pages", methods=['POST'])
def create_page():
    if request.method == 'POST':
        page = {
            'id':0,
            'url':'random_url_for test'
        }
    else:
        abort(400)
    return jsonify({'page': page}), 201

@app.route("/shareit/api/v1.0/links/view/<string:page_url>", methods=['GET'])
@cross_origin()
def get_links_view(page_url):
    print(page_url)
    query = "SELECT * FROM page_links WHERE page_url=(%s);"
    data = (page_url,)
    cursor.execute(query,data)
    if cursor.rowcount > 0:
        columns=['id','url','page_id','page_url']
        results=[]
        for row in cursor.fetchall():
            results.append(dict(zip(columns,row)))
        print(results)
        return make_response(jsonify(results), 200)
    else:
        abort(404)

#handle error 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
