import psycopg2
from pymongo import MongoClient

# MongoDB connection
mongo_client = MongoClient('mongodb+srv://user_hw8:567234@cluster0.yncml3w.mongodb.net/?')
mongo_db = mongo_client['hw8_web']

# PostgreSQL connection
pg_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="567234",
    host="127.0.0.1",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Create tables if they do not exist
pg_cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(255),
        born_date DATE,
        born_location VARCHAR(255),
        description TEXT
    );
""")

pg_cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id SERIAL PRIMARY KEY,
        text TEXT,
        author_id INTEGER REFERENCES authors(id),
        tags TEXT[] DEFAULT ARRAY[]::TEXT[],
        created_at TIMESTAMP
    );
""")

pg_cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        quote_id INTEGER REFERENCES quotes(id)
    );
""")

try:

    # Delete existing data
    pg_cursor.execute("DELETE FROM tags;")
    pg_cursor.execute("DELETE FROM quotes;")
    pg_cursor.execute("DELETE FROM authors;")

    # Commit the deletion
    pg_conn.commit()

    # Migrate authors
    authors = mongo_db.authors.find()
    for author in authors:
        pg_cursor.execute(
            "INSERT INTO authors (fullname, born_date, born_location, description) VALUES (%s, %s, %s, %s) RETURNING id",
            (author['fullname'], author['born_date'], author['born_location'], author['description'])
        )
        author_id = pg_cursor.fetchone()[0]

        # Migrate quotes
        quotes = mongo_db.quotes.find({"author": author["_id"]})
        for quote in quotes:
            pg_cursor.execute(
                "INSERT INTO quotes (text, author_id, tags, created_at) VALUES (%s, %s, %s, NOW()) RETURNING id",
                (
                    quote['quote'],
                    author_id,
                    quote.get('tags', []) if quote.get('tags') is not None else []
                )
            )
            quote_id = pg_cursor.fetchone()[0]

            # Migrate tags
            for tag in quote.get('tags', []):
                pg_cursor.execute(
                    "INSERT INTO tags (name, quote_id) VALUES (%s, %s)",
                    (tag, quote_id)
                )

    # Commit the transaction
    pg_conn.commit()

except Exception as e:
    print(f"Error: {e}")
    # Additional error handling or logging if needed

finally:
    # Close connections
    pg_cursor.close()
    pg_conn.close()
    print("Migration to PostgreSQL successful")
