import urllib3
from flask import Flask, request, after_this_request, send_file
import gzip
import functools
import json
import certifi
from imagepy.image_text import draw_image
from urllib3.util.url import parse_url


app = Flask(__name__)


http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

base_github_url = "https://api.github.com/repos"

headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
    'Content-Type': 'text/plain; charset=utf-8 ',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,vi;q=0.6',
    'Cookie': '_octo=GH1.1.410384889.1403930039; logged_in=yes; dotcom_user=tuanchauict; _ga=GA1.2.1332205087.1380126985',
}


def gzipped(f):
    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if response.status_code < 200 or response.status_code >= 300 or 'Content-Encoding' in response.headers:
                return response

            response.data = gzip.compress(response.data)
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func

@app.route('/')
def home():
    return "Hello world"

@app.route('/service/star')
def get_stars():
    url = request.args.get('url', None)
    if not url:
        return 'Not found', 404

    url = parse_url(url)
    pattern = request.args.get('type', None)
    if url.host == 'github.com':
        (watches, stars, folks) = load_info(url.path)
        if pattern == None:
            return response_stars_image(watches, stars, folks)
        else:
            return response_stars_image(live_or_not(pattern, 'watch', watches), live_or_not(pattern, 'star', stars), live_or_not(pattern, 'folk', folks))

    return "Not found", 404


def live_or_not(pattern, _type, value):
    if _type in pattern:
        return value 
    else:
        return None


def load_info(repo):
    res = http.request('GET', base_github_url + repo, headers=headers)
    if res.status != 200:
        return "Not found", 404
    content = res.data
    data = json.loads(content.decode('utf8'))

    return (data['subscribers_count'], data['stargazers_count'], data['forks_count'])
    

def response_stars_image(watches, stars, folks):
    imgio = draw_image(watches, stars, folks, save=False)

    return send_file(imgio, "image/png")


# --------------TEST GCALL------------------

import time

@app.route('/staff/login', methods=['POST', 'GET'])
def staff_login():
    # time.sleep(2)
    print(request.form)
    print(request.args)
    return json.dumps({
        'status': 'OK',
        'skey': 'test_key'
        }) + "\n"

@app.route('/staff/logout', methods=['GET'])
def staff_logout():
    time.sleep(1)
    print(request.args)
    return json.dumps({
        'status': 'OK'
        }) + "\n"



@app.route('/staff/ready', methods=['GET'])
def staff_ready():
    time.sleep(1)
    print(request.args)
    return json.dumps({
        'status': 'OK',
        'cinfo': {
            'name': 'CustomerX',
            'ckey': 'customerXkey',
            'signalC': {
                'key': "blahblah"
            }
        }
        }) + "\n"

@app.route('/staff/connecting', methods=['GET'])
def staff_connecting():
    time.sleep(1)
    print(request.args)
    return json.dumps({
        'status': 'OK'
        }) + "\n"

def staff_connected():
    time.sleep(1)
    print(request.args)
    return json.dumps({
        'status': 'OK'
        }) + "\n"

def staff_finish():
    time.sleep(1)
    print(request.args)
    return json.dumps({
        'status': 'OK'
        }) + "\n"

# ------------------END TEST GCALL---------------



if __name__ == '__main__':
	import os
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=False, host='0.0.0.0', port=port)