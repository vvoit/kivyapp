import requests
import json
import sqlite3


class Parser:
    def __init__(self):
        self.url = 'https://financialmodelingprep.com/api/v3/stock/actives'
        self.r = requests.get(self.url, stream=True)
        self.json_file = 'data.json'
        self.conn = sqlite3.connect('companies.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS companies
         (id integer primary key, company_name text, price text)''')
        self.conn.commit()

    def get_data(self):
        with open(self.json_file, 'bw') as f:
            for chunk in self.r.iter_content(8192):
                f.write(chunk)

    def parse_data(self):
        with open(self.json_file, 'r') as f:
            data = json.load(f)

        for i in data["mostActiveStock"]:
            self.insert_data(i["companyName"], i["price"])

    def insert_data(self, name, price):
        self.c.execute('''INSERT INTO companies(company_name, price) VALUES (?, ?)''', (name, price))
        self.conn.commit()