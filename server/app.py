from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin
import psycopg2
import os, random, string
from datetime import datetime, timezone


def db_connect():
    connection = psycopg2.connect(host='localhost',
                                database='shareit_db',
                                user=os.environ['POSTGRES_USERNAME'], 
                                password=os.environ['POSTGRES_PASSWORD'])
    return connection
def db_commit(connection):
    connection.commit()
def db_close(connection):
    connection.close()
def db_cursor(connection):
    return connection.cursor()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def home():
    return "Hello, you're home!"

#get all links
@app.route("/shareit/api/v1.0/links", methods=['GET'])
@cross_origin()
def get_links():#возвращает все возможные ссылки из БД
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM link;")
    columns=['id','url','page_id']
    results=[]
    for row in cursor.fetchall():
        results.append(dict(zip(columns,row)))
    connection.close()
    return make_response(jsonify({'links': results},200))

@app.route("/shareit/api/v1.0/pages", methods=['GET'])
@cross_origin()
def get_pages():#возвращает все возможные страницы из БД
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM page;")
    columns=['id','url','creation_time']
    results=[]
    for row in cursor.fetchall():
        results.append(dict(zip(columns,row)))
    connection.close()
    return make_response(jsonify({'pages': results},200))
#get link by id
"""
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
"""
@app.route("/shareit/api/v1.0/links", methods=['POST'])
@cross_origin()
def create_link():
    if request.method == 'POST':
        connection = db_connect()
        cursor = connection.cursor()
        post_data = request.get_json()
        query = "INSERT INTO link (url, description, page_id) VALUES (%s, %s, %s);"
        data = (post_data['url'], post_data['description'], post_data['page_id'])
        print(data)
        cursor.execute(query,data)
        connection.commit()
        connection.close()
    else:
        abort(400)
    return make_response(jsonify({'result': 'OK'}), 201)#http resourse created

#create empty page
@app.route("/shareit/api/v1.0/pages", methods=['POST'])
def create_page():
    this_page_id = None
    this_page_url = None
    if request.method == 'POST':
        connection = db_connect()
        cursor = connection.cursor()
        query = "INSERT INTO page (url, creation_time) VALUES (%s, %s) RETURNING id;"
        this_page_url = make_url()
        data = (this_page_url, datetime.now(timezone.utc))
        cursor.execute(query,data) 
        this_page_id = cursor.fetchone()[0]     
        connection.commit()
        connection.close()
        print(data)        
    else:
        abort(400)
    return make_response(jsonify({'id': this_page_id, 'url': this_page_url}),201)#http resourse created

def make_url():
    return (''.join(random.choices(string.ascii_lowercase, k=10)))
#get view of links by page_url
@app.route("/shareit/api/v1.0/links/view/<string:page_url>", methods=['GET'])
@cross_origin()
def get_links_view(page_url):
    connection = db_connect()
    cursor = connection.cursor()
    print(page_url)
    query = "SELECT * FROM vpage_link WHERE page_url=(%s);"
    data = (page_url,)
    cursor.execute(query,data)
    if cursor.rowcount > 0:
        columns=['id','url','description','page_id','page_url', 'page_creation_time']
        results=[]
        for row in cursor.fetchall():
            results.append(dict(zip(columns,row)))
        print(results)
        connection.close()
        return make_response(jsonify(results), 200)
    else:
        connection.close()
        abort(404)

#handle error 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
