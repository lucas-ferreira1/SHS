from flask import Blueprint, render_template, request, jsonify, session, redirect
from bson.json_util import dumps
from pymongo import MongoClient
from bson.objectid import ObjectId
from functools import wraps
import os
import jinja2

routes = Blueprint('routes', __name__)

MONGO_URI = os.environ['PELS_MONGO_URL']
client = MongoClient(MONGO_URI)
db = client.pelsiasdb
posts = db.posts
sugestions = db.sugestions

template_dir = os.path.join(os.path.dirname(__file__), '../client/templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/blog')
def blog():
    template = jinja_env.get_template('Blog.html')

    return template.render(actual_page=1, previous_page=0, next_page=2)

@routes.route('/blog/<page>')
def blog_page(page):
    template = jinja_env.get_template('Blog.html')

    return template.render(actual_page=page, previous_page=int(page)-1, next_page=int(page)+1)

@routes.route('/blog/posts/<post_id>')
def get_post(post_id):
    post = posts.find({'_id':ObjectId(post_id)}, {'title':1, 'content':1, 'views':1, 'date':1})

    queryRes = []
    for x in post:
        queryRes.append({'id':str(x['_id']), 'title': x['title'], 'content': x['content'], 'views': x['views'], 'date': x['date'].date()})

    # print(queryRes)

    template = jinja_env.get_template('blog-post.html')

    return template.render(title=queryRes[0]["title"], content=queryRes[0]["content"])

@routes.route('/contato')
def contato():
    return render_template('contato.html')   
    
@routes.route('/diretoria')
def diretoria():
    return render_template('diretoria.html')

@routes.route('/join-us')
def join_us():
    return render_template('join-us.html')

@routes.route('/marketing')
def marketing():
    return render_template('marketing.html')

@routes.route('/membros')
def membros():
    return render_template('membros.html')

@routes.route('/projetos')
def projetos():
    return render_template('projetos.html')

@routes.route('/atividades_academicas')
def attividades_academicas():
    return render_template('atividades_academicas.html')

@routes.route('/login')
def login():
    return render_template('login.html')

@routes.route('/addposts')
@login_required
def add_posts():
    return render_template('addposts.html')

@routes.route('/test')
def test():
    collection.insert({'_teste' : 'ola teste'})
    return 'HELLO WORLD'