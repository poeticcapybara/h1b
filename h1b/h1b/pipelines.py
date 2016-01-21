# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class H1BPipeline(object):
    def __init__(self):
        self.setupDBCon()
        self.createTables()

    def setupDBCon(self):
        self.con = sqlite3.connect('./h1b.db') #Change this to your own directory
        self.cur = self.con.cursor()

    def createTables(self):
		# self.dropVisasTable()
		# self.dropEmployerTable()
		# self.dropJobTable()
		# self.dropLocationTable()

		self.createVisasTable()
		self.createEmployerTable()
		self.createJobTable()
		self.createLocationTable()

    def createEmployerTable(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Employer (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE
        );
        ''')

    def createJobTable(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Jobtitle (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE
        );
        ''')

    def createLocationTable(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Location (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            city TEXT UNIQUE,
            state TEXT
        );
        ''')

    def createVisasTable(self):

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Visas (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            employer_id INTEGER,
            jobtitle_id INTEGER,
            location_id INTEGER,
            salary INTEGER,
            submit_date TEXT,
            start_date TEXT,
            status TEXT
        );
        ''')

    def dropEmployerTable(self):
        self.cur.execute("DROP TABLE IF EXISTS Employer")

    def dropJobTable(self):
        self.cur.execute("DROP TABLE IF EXISTS Jobtitle")

    def dropLocationTable(self):
        self.cur.execute("DROP TABLE IF EXISTS Location")

    def dropVisasTable(self):
        self.cur.execute("DROP TABLE IF EXISTS Visas")

    def process_item(self, item, spider):
        employer_id = self.storeInEmployerDb(item)
        jobtitle_id = self.storeInJobDb(item)
        location_id = self.storeInLocationDb(item)
        self.storeInVisasDb(item, employer_id, jobtitle_id, location_id)
        return item

    def storeInEmployerDb(self, item):
        employer = item.get('employer','')
        self.cur.execute("INSERT OR IGNORE INTO Employer(\
            name\
            ) \
        VALUES( ? )", \
        (employer,)\
                         )
        print '------------------------'
        print 'Employer Stored in Database'
        print '------------------------'
        self.cur.execute('SELECT id FROM Employer WHERE name = ? ', (employer, ))
        employer_id = self.cur.fetchone()[0]
        self.con.commit()
        return employer_id

    def storeInJobDb(self, item):
        jobtitle = item.get('jobtitle','')
        self.cur.execute("INSERT OR IGNORE INTO Jobtitle(\
            name\
            ) \
        VALUES( ? )", \
        (jobtitle,)\
                         )
        print '------------------------'
        print 'Job Title Stored in Database'
        print '------------------------'
        self.cur.execute('SELECT id FROM Jobtitle WHERE name = ? ', (jobtitle, ))
        jobtitle_id = self.cur.fetchone()[0]
        self.con.commit()
        return jobtitle_id

    def storeInLocationDb(self, item):
        city = item.get('city','')
        state = item.get('state','')
        self.cur.execute("INSERT OR IGNORE INTO Location(\
            city, \
            state \
            ) \
        VALUES( ?, ? )", \
        (city, state)\
                         )
        print '------------------------'
        print 'Location Stored in Database'
        print '------------------------'
        self.cur.execute('SELECT id FROM Location WHERE city = ? ', (city, ))
        location_id = self.cur.fetchone()[0]
        self.con.commit()
        return location_id

    def storeInVisasDb(self, item, employer_id, jobtitle_id, location_id):
        self.cur.execute("INSERT OR REPLACE INTO Visas(\
            employer_id, \
            jobtitle_id, \
            location_id, \
            salary,\
            submit_date,\
            start_date,\
            status \
            ) \
        VALUES( ?, ?, ?, ?, ?, ?, ?)", \
        ( \
            employer_id,
            jobtitle_id,
            location_id,
            item.get('salary',''),
            item.get('submitdate',''),
            item.get('startdate',''),
            item.get('status','')
        ))
        print '------------------------'
        print 'Visa Stored in Database'
        print '------------------------'
        self.con.commit()

    def closeDB(self):
        self.con.close()

    def __del__(self):
        self.closeDB()
