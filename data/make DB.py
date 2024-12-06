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

data = [("кофе", "медиум", "зерно", "вкусно", "0", "0"),
        ("обемарикано", "медиум", "порошок", "вкусно", "100000", "1"),
        ("лодкэ", "медиум", "зерно", "пипец как вкусно", "10", "100"),
        ("кофэ", "медиум", "зерно", "очень вкусно", "1000", "150"),
        ("рафт", "минимум", "зерно", "не вкусно", "1", "100"),]

# добавляет админа
with con:
    for s_data in data:
        con.execute(sql, s_data)

# вывод всех пользователей и их данных
with con:
    data = con.execute("""SELECT * FROM coffe""")
    for row in data:
        print(row)
