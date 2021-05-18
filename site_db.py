import sqlite3

con = sqlite3.connect('patterns.sqlite')
crsr = con.cursor()
with open('site_db.sql', 'r') as f:
    text = f.read()
crsr.executescript(text)
crsr.close()
con.close()
