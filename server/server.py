from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import jwt
import datetime
from functools import wraps
from slackclient import SlackClient
import os
from googleapiclient.discovery import build
from pymongo import MongoClient
import optparse
import sys

parser = optparse.OptionParser()
parser.add_option('--mongourl', action='store', dest='mongodb_url', help='MongoDB URL')
parser.add_option('--slackchannel', action='store', dest='slack_channel', help='Slack channel id')
parser.add_option('--slacktoken', action='store', dest='slack_token', help='Slack API token')
parser.add_option('--googlekey', action='store', dest='google_key', help='Google CSE API key')
parser.add_option('--googlecse', action='store', dest='google_cse_id', help='Google CSE id')

options, args = parser.parse_args()

if not options.mongodb_url:
    sys.exit('--mongourl flag missing')
if not options.slack_channel:
    sys.exit('--slackchannel flag missing')
if not options.slack_token:
    sys.exit('--slacktoken flag missing')
if not options.google_key:
    sys.exit('--googlekey flag missing')
if not options.google_cse_id:
    sys.exit('--googlecse flag missing')


""" *************************************************
Initial configuration.

Some of the parameters contain sensitive information,
therefore it would be optimal to pass these params via
the console during initialization of the Python app.

To keep data private, use the os.environ library to
access to this info passed by flags.
************************************************* """
app = Flask(__name__)

# Used to encode/decode the JWT token
app.config['SECRET_KEY'] = 'somesecretkey'

# A fake username
app.config['USERNAME'] = 'username'
# A fake password
app.config['PASSWORD'] = 'password'

# The mongodb conection URL
app.config['MONGO_CONN_URL'] = options.mongodb_url

# Slack configuration
app.config['SLACK_CHANNEL_ID'] = options.slack_channel
app.config['SLACK_TOKEN'] = options.slack_token

# Google configuration
app.config['GOOGLE_API_KEY'] = options.google_key
app.config['GOOGLE_CSE_ID'] = options.google_cse_id

api = Api(app)


# print os.environ['FOO']



""" *************************************************
Generates a response message with a code number.
************************************************* """
def message_gen(message, code=200):
    return {'message': message}, code



""" *************************************************
This decorator function is used to authenticate routes.
************************************************* """
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return message_gen('Token is missing', 403)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return message_gen('Token is invalid', 403)

        return func(*args, **kwargs)
    return wrapper



""" *************************************************
Used to authenticate routes.
************************************************* """
def tokens_generator(username):
    token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, app.config['SECRET_KEY'])
    refresh = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)}, app.config['SECRET_KEY'])
    return { 'token': token, 'refresh': refresh }



""" *************************************************
Stores docs in MongoDB
************************************************* """
def format_mongo_search_doc(request):
    return {
        'event': 'search',
        'cat': request.args.get('cat'),
        'query': request.args.get('query'),
        'timestamp': datetime.datetime.utcnow(),
        'username': app.config['USERNAME'],
        'client_ip': request.environ['REMOTE_ADDR']
    }

def format_mongo_login_doc(request, ok=False):
    return {
        'event': 'login',
        'timestamp': datetime.datetime.utcnow(),
        'username': app.config['USERNAME'],
        'client_ip': request.environ['REMOTE_ADDR'],
        'ok': ok
    }

def format_mongo_refresh_doc(request, ok=False):
    return {
        'event': 'refresh',
        'timestamp': datetime.datetime.utcnow(),
        'username': app.config['USERNAME'],
        'client_ip': request.environ['REMOTE_ADDR'],
        'ok': ok
    }

def format_mongo_event_doc(request):
    return {
        'event': 'view',
        'timestamp': datetime.datetime.utcnow(),
        'username': app.config['USERNAME'],
        'client_ip': request.environ['REMOTE_ADDR'],
        'thumbnail': request.args.get('thumbnail'),
        'description': request.args.get('description'),
        'url': request.args.get('url'),
        'cat': request.args.get('cat'),
        'query': request.args.get('query')
    }

def store_mongo_doc(doc):
    client = MongoClient(app.config['MONGO_CONN_URL'])
    db = client['galacticsearchengine']
    collection = db.logs
    collection.insert_one(doc)



""" *************************************************
This URI sends a message to Slack and saves a doc to
mongodb everytime an event is triggered on the client.

This route is protected.

This route takes in an event name (view, click, close, etc).
************************************************* """
def build_slack_client():
    slack_token = app.config['SLACK_TOKEN']
    return SlackClient(slack_token)

def send_slack_message(text, attachments=None):
    slack_client = build_slack_client()

    params = { 'channel': app.config['SLACK_CHANNEL_ID'], 'text': text }

    if not attachments:
        return slack_client.api_call(
            "chat.postMessage",
            **params
        )

    return slack_client.api_call(
        "chat.postMessage",
        attachments=attachments,
        **params
    )

def format_slack_login_message(doc):
    return 'A login message'
def send_slack_login_message(request, ok=False):
    doc = format_mongo_login_doc(request, ok)
    store_mongo_doc(doc)
    slack_message = format_slack_login_message(doc)
    send_slack_message(slack_message)

def format_slack_refresh_message(doc):
    return 'A refresh message'
def send_slack_refresh_message(request, ok=False):
    doc = format_mongo_refresh_doc(request, ok)
    store_mongo_doc(doc)
    slack_message = format_slack_refresh_message(doc)
    send_slack_message(slack_message)

def format_slack_search_message(doc):
    return 'A search message'
def send_slack_search_message(request):
    doc = format_mongo_search_doc(request)
    store_mongo_doc(doc)
    slack_message = format_slack_search_message(doc)
    send_slack_message(slack_message)

def format_slack_event_message(doc):
    return {
        'text': 'An event message with attachments',
        'attachments': [
            {
                'fallback': "url: {} - description: {} - at {}".format(doc['url'], doc['description'], doc['timestamp']),
                'thumb_url': doc['thumbnail'],
                'color': '#36a64f',
                'pretext': '{} triggered a {} at {}'.format(doc['client_ip'], doc['event'], doc['timestamp']),
                'title': doc['cat'],
                'text': doc['description']
            }
        ]
    }
def send_slack_event_message(request):
    doc = format_mongo_event_doc(request)
    slack_message = format_slack_event_message(doc)
    print slack_message
    send_slack_message(**slack_message)

class Event(Resource):
    method_decorators = [authenticate]

    def post(self):
        thumbnail = request.args.get('thumbnail')
        description = request.args.get('description')
        url = request.args.get('url')
        cat = request.args.get('cat')
        query = request.args.get('query')

        if not thumbnail:
            return message_gen('thumbnail is missing in query string', 403)
        if not description:
            return message_gen('description is missing in query string', 403)
        if not url:
            return message_gen('url is missing in query string', 403)
        if not cat:
            return message_gen('cat is missing in query string', 403)
        if not query:
            return message_gen('query is missing in query string', 403)
        try:
            send_slack_event_message(request)
            return message_gen('Message sent')
        except:
            return message_gen('Unable to send message to slack', 403)



""" *************************************************
Allows users to login with username and
password. This will issue a new token and a refresh
token.

The duration for the token is of 1 minute
The duration for the refresh is of on year
This route is not protected.

This route takes in the username and password via query
params.
************************************************* """
class Login(Resource):
    def post(self):
        auth = request.authorization

        if auth and auth.username == app.config['USERNAME'] and auth.password == app.config['PASSWORD']:
            send_slack_login_message(request, True)
            return tokens_generator(auth.username)

        send_slack_login_message(request)

        return message_gen('Invalid username or password', 403)



""" *************************************************
Allows users to refresh expired tokens as
long as they have a valid refresh token.

This will issue a new set of tokens.
This route is not protected.

This route takes in a token via query
params.
************************************************* """
class Refresh(Resource):
    def post(self):
        token = request.args.get('token')

        if not token:
            return message_gen('Token is missing', 403)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            send_slack_refresh_message(request, True)
            return tokens_generator(data['username']), 200
        except:
            send_slack_refresh_message(request, False)

            return message_gen('The refresh token is invalid', 403)



""" *************************************************
Allows users to perform search queries to
Google APIs (text, images and videos).

This route is not protected.

This route takes in a category and a criteria via query
params.
************************************************* """
def build_cse(cat='', query='', limit=4):
    api_key = app.config['GOOGLE_API_KEY']
    service_name = 'customsearch'
    service = build(service_name, 'v1', developerKey=api_key)
    cse_id = app.config['GOOGLE_CSE_ID']
    return service.cse().list(q=cat + query, num=limit, cx=cse_id, searchType="image")

def build_yt(cat='', query='', limit=1):
    api_key = app.config['GOOGLE_API_KEY']
    service_name = 'youtube'
    api_version = 'v3'
    service = build(service_name, api_version, developerKey=api_key)
    return service.search().list(
        q = cat + query,
        part = 'id, snippet',
        maxResults = 1
    )

class Search(Resource):
    method_decorators = [authenticate]

    def post(self):
        cat = request.args.get('cat')
        query = request.args.get('query')

        if not cat:
            return message_gen('cat query param is missing', 403)
        if not query:
            query = ''
        try:
            cse_results = build_cse(cat, query).execute()
            yt_results = build_yt(cat, query).execute()

            send_slack_search_message(request)

            return { 'images': cse_results['items'], 'videos': yt_results['items'] }, 200
        except:
            return message_gen('Unable to perform search', 403)



""" *************************************************
************************************************* """
api.add_resource(Login, '/login')
api.add_resource(Refresh, '/refresh')
api.add_resource(Search, '/search')
api.add_resource(Event, '/events')



if __name__ == '__main__':
    app.run(debug=True)
