1) Install sqlite3:
	$: sudo apt install sqlite3

2) Determine the SQLite folder:
	$: which sqlite3 
	/usr/bin/sqlite3

3) Change DB variable and adapt to your DB path (e.g. "/home/vt/sqlite3_db/local_omdb.db") or place it in the python project folder ("/home/vt/PycharmProjects/omdb") 

4) Run script create_db.py or create database manualy from SQLite CLI

5) Go into the folder:
	$: cd sqlite3_db/

6) Assign user and group to the DB file:
	$: sudo chown vt:vt local_omdb.db

7) Assign permissions to the DB file:
	$: sudo chmod 664 *

8) Jump into SQLite CLI:
	$: sqlite3 local_omdb.db 

9) Enable header for your table:
	sqlite> .headers on

10) Determine column width:
	 sqlite> .width 10 25 3 6 15

11) Allign columnt for better view:
	 sqlite> .headers column

12) Open our database:
	 sqlite> .open local_omdb.db

13) Check all tables in the database:
	 sqlite> .tables

14) Output all rows:
	 sqlite> select * from films;

15) Delete all rows (for testing purpose):
	 sqlite> DELET FROM films WHERE rowid < 8000;