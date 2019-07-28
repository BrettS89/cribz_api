import sqlite3
from services.crib import scrape

class CribModel:
    def __init__(self, url, user, _id):
        crib_details = CribModel.get_details(url)
        self.url = url
        self.name = crib_details['name']
        self.price = crib_details['price']
        self.pictures = crib_details['pictures']
        self.user = user
        
        if _id:
            self.id = _id
        else:
            self.id = None

    @classmethod
    def get_details(cls, url):
        return scrape(url)

    def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name,
            'price': self.price,
            'pictures': self.pictures,
            'user': self.user
        }

    def save_to_db(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO cribs VALUES (NULL, ?, ?, ?, ?, ?)'
        cursor.execute(query, (self.url, self.name, self.price, self.pictures, self.user))

        connection.commit()
        connection.close()
        self.get_by_url(self.url)

    def get_by_id(self, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM cribs WHERE id=?'
        results = cursor.execute(query, (_id,))
        row = results.fetchone()

        self.id = row[0]
        self.url = row[1]
        self.name = row[2]
        self.price = row[3]
        self.pictures = row[4]
        self.user = row[5]

        connection.close()

    def get_by_url(self, url):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM cribs WHERE url=?'
        results = cursor.execute(query, (url,))
        row = results.fetchone()

        self.id = row[0]
        self.url = row[1]
        self.name = row[2]
        self.price = row[3]
        self.pictures = row[4]
        self.user = row[5]

        connection.close()

    def delete_from_db(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM cribs WHERE id=?'
        cursor.execute(query, (self.id,))
        cursor.commit()
        connection.close()
