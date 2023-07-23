import sqlite3


def return_books() :
	conn = sqlite3.connect('library_db.db')
	return (conn.execute("SELECT book_id, book_name, book_author FROM Books"))
	conn.close()