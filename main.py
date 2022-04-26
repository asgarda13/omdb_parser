import json
import requests
import sqlite3
from sqlite3 import Error
import numpy as np
from time import sleep
from random import uniform
import time

header = {"Content-Type": "application/json"}
database = r"/home/vt/sqlite3_db/local_omdb.db"
web_host = "http://www.omdbapi.com/?"
api_token = "apikey=2701f86c"
movies_Title = []
movies_Date = []
imdbID = []
last_page_response = {'Response': 'False', 'Error': 'Movie not found!'}
err_input_response = {'Response': 'False', 'Error': 'Too many results.'}
pages = np.arange(1, 1000, 1)


def movie_name_precheck():
    """ This function is called to check if the movie name and response is correct. 
    :return: checkedname - correct name
    """
    checkedname = ''
    name = False
    while not name:
        movie_name = input("Input movie name (* can be used): ").strip()
        url_input_check = f"{web_host}{api_token}&plot=short&type=movie&s={movie_name}&page=1"
        resp_input_check = requests.get(url_input_check, headers=header)
        if last_page_response == resp_input_check.json():
            print(f"ERROR: Movie not found or wrong input!")
        elif err_input_response == resp_input_check.json():
            print(f"ERROR: Too many results! Try more that 2 characters.")
        else:
            checkedname = movie_name
            name = True
        if not resp_input_check.ok:  # if response not 200
            print(resp_input_check.text)
            exit(1)
    return checkedname

def parse_movie(checkedname):
    """ This function will parse OMDB API with mentioned correct movie name
    :param checkedname: from input
    :return: the list of prepared rows (Title, Year, IMDB_ID). Array = Python List type
    """
    movty = []
    for c, page in enumerate(pages):
        page = f"{web_host}{api_token}&plot=short&type=movie&s={checkedname}&page=" + str(page)  # looping each page with needed keyword
        response = requests.get(page, headers=header)
        # sleep(uniform(0.05,0.1))  # Delay, if there are restrictions for amount of calls.
        if last_page_response == response.json():
            print(f"There are {c + 1} pages for your search in the OMDB")
            break
        for item in json.loads(response.text)['Search']:  # looping thought items on each page
            movies_Title.append(item['Title'])
            movies_Date.append(item['Year'])
            imdbID.append(item['imdbID'])
            movty = list(zip(movies_Title, movies_Date, imdbID))  # Appending all items in one list
    movty.sort()  # Sorting by movie title
    return movty


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def insert_movie(conn, movty):
    """
    Insert a new movie into the films table
    :param conn:
    :param movty:
    :return: ...
    """
    sql = ''' INSERT INTO films(title,year,imdb_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    for item in movty:
        cur.execute(sql, item)
    conn.commit()


def sqlite_films_tab_output(conn):
    """
    Attention! Insecure output "*", only for tests.
    :param conn:

    For better output in SQLite use the following parameters:
    .headers on
    .width 5 55 5 12
    .mode column
    """
    sql_all = '''SELECT * FROM films'''
    cur = conn.cursor()
    cur.execute(sql_all)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def main():
    print("")
    print("This script will search movies in OMDB (Open Movie Data Base)")
    checkedname = movie_name_precheck()
    tic = time.perf_counter()  # Used to count script performance
    movty = parse_movie(checkedname)  # Feeding a parsing function with the correct and existing name

    conn = create_connection(database)  # Create a database connection
    with conn:
        try:
            insert_movie(conn, movty)  # Inserting movies from the parsed and sorted list into the SQLite DB
            print('-' * 16, 'Films found:', '-' * 16)
            i = 0
            for i, index in enumerate(movty):
                print(f'{i+1}) "{index[0]}", {index[1]}')
                if i == 29:
                    print(len(movty)-i-1,'rows skipped.')
                    break
            print('-' * 11, len(movty), 'added to the DB', '-' * 11)
            # films_table_output(conn)  # Insecure! Checking DB output, only for test.
        except Error as insert_err:
            print("Error! cannot insert to the database.")
            print(insert_err)
    toc = time.perf_counter()
    print('\n', f"The script performance is {toc - tic:0.4f} seconds")


if __name__ == '__main__':
    main()
