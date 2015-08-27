import sqlite3

with sqlite3.connect('fruits.db') as connection:
    c = connection.cursor()
    #c.execute("DROP TABLE farmer")
    c.execute("CREATE TABLE farmer(fruit TEXT, farmer TEXT, state TEXT)")
    c.execute('INSERT INTO farmer VALUES("Apples", "Bob", "Florida")')
    c.execute('INSERT INTO farmer VALUES("Bananas", "Joe", "California")')
    c.execute('INSERT INTO farmer VALUES("Oranges", "Bob", "Texas")')
    c.execute('INSERT INTO farmer VALUES("Carrots", "Frank", "Maine")')
    c.execute('INSERT INTO farmer VALUES("Berries", "Frank", "Maine")')
    c.execute('INSERT INTO farmer VALUES("Grapes", "Kelly", "Kansas")')