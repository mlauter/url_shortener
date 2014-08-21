from flask import Flask, request, render_template, url_for, redirect
from collections import defaultdict

app = Flask(__name__)

last_key = ''
hash_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c",
"d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
"t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I",
"J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
"Z"]
url_map={}

@app.route('/', methods = ['GET'])
@app.route('/index', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/new_url', methods = ['POST'])
def display_new_url():
    print request.form['url']
    raw_url = request.form['url']
    print raw_url
    global last_key
    last_key = hash_fun(last_key)
    url_map[last_key] = raw_url
    short_url = 'http://10.0.5.236:5000/' +last_key
    return render_template('new_url.html', new_url=short_url)

@app.route('/<key>', methods=['GET'])
def redirector(key):
    try:
        real_url = url_map[key]
        return redirect(real_url,code=302)
    except:
        return redirect(url_for('page_not_found'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


def hash_fun(last_key):
    if last_key == '':
        return '1'

    ticker = last_key[-1]
    ticker_ind = hash_chars.index(ticker) + 1
    ticker_ind %= len(hash_chars)

    if ticker_ind==0:
        return hash_fun(last_key[:-1]) + '0'
    else:
        return last_key[:-1] + hash_chars[ticker_ind]




if __name__ == "__main__":     
    app.run('0.0.0.0')
