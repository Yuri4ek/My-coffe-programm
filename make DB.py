import sqlite3 as sql

con = sql.connect("coffee.sqlite")

# создает таблицу паролей
with con:
    data = con.execute("""SELECT count(*) FROM sqlite_master 
                        WHERE type='table' and name='coffe'""")
    for row in data:
        if row[0] == 0:
            with con:
                con.execute("""
                    CREATE TABLE coffe 
                    (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
                        nameVariety, 
                        degreeRoasting, 
                        groundGrains, 
                        descriptionTaste, 
                        price, 
                        packingVolume
                    );
                """)

# удаляет всех клиентов
with con:
    con.execute("""DELETE FROM coffe""")

sql = """INSERT INTO coffe 
        (nameVariety, degreeRoasting, groundGrains, 
        descriptionTaste, price, packingVolume) values(?, ?, ?, ?, ?, ?)"""

data = ("кофе", "медиум", "зерно", "вкусно", "0", "0")

# добавляет админа
with con:
    con.execute(sql, data)

# вывод всех пользователей и их данных
with con:
    data = con.execute("""SELECT * FROM coffe""")
    for row in data:
        print(row)