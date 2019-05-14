# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


class HdrezkaPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()


    def create_connection(self):
        self.conn = sqlite3.connect('films.db')
        self.curr = self.conn.cursor()


    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS films_tb""")
        self.execute("""create table films_tb(
                name text,
                date text, 
                rating text,
                director text,
                genre text,
                picture text,
                description text
                )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, items):
        self.curr.execute("""insert into films_db values (?,?,?,?,?,?,?)""",(
            items['name'],
            items['date'],
            items['rating'],
            items['director'],
            items['genre'],
            items['picture'],
            items['description']
        ))
        self.conn.commit()