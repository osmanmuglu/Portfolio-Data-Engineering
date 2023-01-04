import sqlite3

conn = sqlite3.connect('lunch.db')
c = conn.cursor()

c.execute('''DROP TABLE meals''') ###deleting table

c.execute('''CREATE TABLE meals(sandwich TEXT, fruit TEXT, tablenumber INT)''') ###creating table

sandwich = 'chicken'
fruit = 'orange'
tablenum = 22

c.execute('''INSERT INTO meals VALUES(?, ?, ?)''', (sandwich, fruit, tablenum)) ###inserting data into table
conn.commit()

c.execute('''SELECT * FROM meals''')
results = c.fetchall()
print(results)