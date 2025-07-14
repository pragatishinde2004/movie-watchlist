import mysql.connector
from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv
import os

load_dotenv()

def createConnection():
    connection = mysql.connector.connect(
        user = os.environ.get("DB_USER"),
        host = os.environ.get("DB_HOST"),
        database = os.environ.get("DB_NAME"),
        password = os.environ.get("DB_PASSWORD"),

    )
    return connection

web = Flask(__name__)

def createTables():
    connection = createConnection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist(
            id INT AUTO_INCREMENT PRIMARY KEY,
            movies VARCHAR(50), 
            status VARCHAR(50) DEFAULT 'Pending')
    """)
    print("Tables created!!")
    connection.commit()
    connection.close()
    cursor.close()

createTables()

@web.route("/", methods = ['GET','POST'])
def watchMovies():
    connection = createConnection()
    cursor = connection.cursor()
    if request.method == "POST":
        movie = request.form['movies']
        cursor.execute("INSERT INTO watchlist(movies,status) VALUES(%s,%s)",(movie,'Pending'))
        connection.commit()
        cursor.close()
        connection.close()
        redirect('watch_movies.html')
    
    return render_template("watch_movies.html")

@web.route("/viewWatchlist" )
def viewWatchlist():
    connection = createConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM watchlist")
    show = cursor.fetchall()
    connection.close()
    cursor.close()
    return render_template('viewWatchlist.html', movies = show)

@web.route("/watched<int:movie_id>", methods = ['POST'])
def watched(movie_id):
    connection = createConnection()
    cursor = connection.cursor()
    cursor.execute("UPDATE watchlist set STATUS = 'Watched' WHERE id = %s",(movie_id,))
    connection.commit()    
    print("watched")
    connection.close()
    cursor.close()
    return redirect(url_for('viewWatchlist'))

@web.route("/edit<int:movie_id>", methods = ['GET','POST'])
def edit(movie_id):
    connection = createConnection()
    cursor = connection.cursor()
    if request.method == "POST":
        new = request.form['movies']
        cursor.execute("UPDATE watchlist set movies = %s WHERE id = %s",(new,movie_id))
        connection.commit()
        # connection.close()
        return redirect(url_for('viewWatchlist'))
    
    cursor.execute("SELECT movies FROM watchlist WHERE id = %s",(movie_id,))
    data = cursor.fetchone()
    if data :
        data = data[0]
    connection.close()
    # cursor.execute()

    return render_template('movie_edit.html', movie_id=movie_id, movies=data)


@web.route("/remove<int:movie_id>", methods =['POST'])
def remove(movie_id):
    connection = createConnection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM watchlist WHERE id = %s",(movie_id,))
    connection.commit()
    connection.close()
    cursor.close()
    return redirect(url_for('viewWatchlist'))

if __name__ == "__main__":
    web.run(debug=True)