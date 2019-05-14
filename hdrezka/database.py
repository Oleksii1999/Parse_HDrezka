import  sqlite3


conn = sqlite3.connect('films.db')
curr = conn.cursor()

curr.execute("""create table films_tb(
                name text,
                date text, 
                rating text,
                director text,
                genre text,
                picture text,
                description text
                )""")

curr.execute()

conn.commit()
conn.close()