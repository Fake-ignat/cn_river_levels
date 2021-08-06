import sqlite3 as sq

with sq.connect('storage/chinese_levels.db') as con:
    SELECT_DATA = f""" SELECT *
            FROM posts
                """

    CREATE_TABLE_2 = """ CREATE TABLE levels (
            date timestamp,
            cn_name TEXT,
            level REAL
        )  """

    DELETE_ROWS = """
    DELETE FROM levels
            WHERE date='02.08.2021'
    """


    cur = con.cursor()
    cur.execute(DELETE_ROWS)
    for line in cur.fetchall():
        print(line)


CREATE_TABLE = """ CREATE TABLE posts (
        cn_name TEXT PRIMARY KEY,
        ru_name TEXT NOT NULL,
        ru_river TEXT,
        cn_river TEXT,
        critical_level REAL,
        lon REAL,
        lat REAL
    )  """

CREATE_TABLE_2 = """ CREATE TABLE levels (
        date timestamp,
        cn_name TEXT,
        level REAL
    )  """

# INSERT_DATA = f""" INSERT INTO posts
#         (cn_name, ru_name, ru_river, cn_river, critical_level, lon, lat )
#         VALUES ('{p['cn_name']}',
#                 '{p['name']}',
#                 '{p['river']}',
#                 '{p['cn_river']}',
#                 {p['critical'] if p['critical'] else 'NULL'},
#                 {p['lon']},
#                 {p['lat']})
#         """