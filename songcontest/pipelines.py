# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from os import path
 
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class SongcontestPipeline(object):
    def process_item(self, item, spider):
        return item

 
class SQLiteStorePipeline(object):
    filename = 'data.sqlite'
 
    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)
 
    def process_item(self, item, domain):
        try:
            self.conn.execute('insert into votes values(?,?,?,?)', 
                          (item['year'], item['fromParticipant'], item['toParticipant'], item['points']))
        except:
            print 'Failed to insert item: ' + item['fromParticipant'] + '->' + item['toParticipant'] + '(' + str(item['year']) + ')'
        return item
 
    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)
 
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
 
    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""CREATE TABLE votes (year INTEGER NOT NULL, fromParticipant TEXT NOT NULL, toParticipant TEXT NOT NULL, points INTEGER NOT NULL, PRIMARY KEY(year, fromParticipant, toParticipant))""")
        conn.commit()
        return conn
