# import to psycop2 to connect to db
import psycopg2

DBNAME = "news"


def get_items(query):
    """ Returns results based on query passed as a param"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    bd_query = query
    c.execute(bd_query)
    return c.fetchall()
    db.close()
