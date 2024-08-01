from flask import Flask, render_template, url_for, request, redirect, flash;
import sqlite3
import requests
import json


app = Flask(__name__)
app.secret_key = 'meta_minds'

# movies api
API_KEY = '51173b635c9720fa4597bb00a67e112d'
BASE_URL = 'https://api.themoviedb.org/3'

def tmdb_request(endpoint, params={}):
    params['api_key'] = API_KEY
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    return response.json()

# books api
OPEN_LIBRARY_URL = 'https://openlibrary.org'

def open_library_request(endpoint, params={}):
    response = requests.get(f"{OPEN_LIBRARY_URL}/{endpoint}", params=params)
    return response.json()


# database connection 
db_connect =sqlite3.connect('database.db')
print('successeful conection')

# create table in database
db_connect.execute('CREATE TABLE IF NOT EXISTS users (email TEXT,fullname TEXT,username TEXT,password TEXT)')
print('table created')
db_connect.close()

#Route for pages 


# landing page
@app.route('/')
def index():
    return render_template('index.html')

# signup page
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email = request.form['email']
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect('database.db') as db_connect:
            cur = db_connect.cursor()
            cur.execute("INSERT INTO users (email, fullname, username, password) VALUES (?, ?,?,?)", (email,fullname,username, password))
            db_connect.commit()
            return render_template('continue.html')
    return render_template('signup.html')


# signin page
@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('database.db') as db_connect:
            cur = db_connect.cursor()
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user =cur.fetchone()
            if user:
                user_name =username.capitalize()
                # movies
                movies = tmdb_request('movie/popular')['results']

                return render_template('dashboard.html',user_name=user_name, movies = movies)
            else:
                flash ("inavlid username or password")
                return render_template('signin.html')
    return render_template('signin.html')
# books
@app.route('/books', methods=['GET', 'POST'])
def books():
    query_books = "the"
    if request.method == 'POST':
        query_books = request.form.get('query_books', '')
    
    params_books = {'title': query_books}
    results_books = open_library_request('search.json', params_books)['docs']
    books = [{
        'title': book.get('title'),
        'cover_id': book.get('cover_i')
    } for book in results_books[:50]]  # Limiting to 50 books for display
    return render_template('books.html', books=books, query_books=query_books)
    
# search bar url

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        results = tmdb_request('search/movie', {'query': query})['results']
        return render_template('search.html', results=results, query=query)
    return render_template('search.html', results=[], query='')

@app.route('/favorites')
def favorite_movies():
    session_id = 'your_session_id'
    account_id = 'your_account_id'
    endpoint = f'account/{account_id}/favorite/movies'
    params = {'session_id': session_id}
    favorites = tmdb_request(endpoint, params=params)['results']
    return render_template('favorites.html', favorites=favorites)

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    movie_id = request.form['movie_id']
    session_id = 'your_session_id'
    account_id = 'your_account_id'
    endpoint = f'account/{account_id}/watchlist'
    payload = {
        'media_type': 'movie',
        'media_id': movie_id,
        'watchlist': True
    }
    params = {'session_id': session_id}
    response = requests.post(f"{BASE_URL}/{endpoint}", json=payload, params=params)
    return redirect(url_for('signin page'))


# continue page
@app.route('/continuepage2')
def continuePage2():
    return render_template('continuepage2.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')




if __name__=='__main__':
     app.run(debug=True)