import sqlite3


conn = sqlite3.connect('replay.db')
cursor = conn.cursor()
cursor.execute(
    'create table replay (id INTEGER  primary key AUTOINCREMENT, replay_id int, hero varchar(20), opp_hero varchar(20), date TEXT)'
)

conn.commit()
cursor.close()
conn.close()