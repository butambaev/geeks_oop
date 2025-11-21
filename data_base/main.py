import sqlite3

conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    director TEXT,
    year INTEGER,
    genre TEXT,
    rating REAL
)
''')

conn.commit()
conn.close()

def add_movie(title, director, year, genre, rating):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO movies (title, director, year, genre, rating) VALUES (?, ?, ?, ?, ?)',
                   (title, director, year, genre, rating))
    conn.commit()
    conn.close()

def get_movies():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    conn.close()
    return movies

def update_movie(movie_id, title=None, director=None, year=None, genre=None, rating=None):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    fields = []
    values = []
    if title:
        fields.append("title = ?")
        values.append(title)
    if director:
        fields.append("director = ?")
        values.append(director)
    if year:
        fields.append("year = ?")
        values.append(year)
    if genre:
        fields.append("genre = ?")
        values.append(genre)
    if rating:
        fields.append("rating = ?")
        values.append(rating)
    values.append(movie_id)
    cursor.execute(f'UPDATE movies SET {", ".join(fields)} WHERE id = ?', values)
    conn.commit()
    conn.close()

def delete_movie(movie_id):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    conn.commit()
    conn.close()

add_movie("Interstellar", "Christopher Nolan", 2014, "Sci-Fi", 9.0)
add_movie("The Matrix", "Wachowski", 1999, "Sci-Fi", 8.7)

print(get_movies())

update_movie(1, rating=9.5)

print(get_movies())

delete_movie(2)

print(get_movies())
