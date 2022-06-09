import os
import sqlite3

# 数据库连接
def get_conn(model_track_path):
    return sqlite3.connect(os.path.join(model_track_path, 'model_track_center.db'))

import os

def create_tables(model_track_path):
    conn = get_conn(model_track_path)
    sql_script = open(os.path.join("./", 'db.sql'), 'r', encoding='utf-8').read()
    conn.executescript(sql_script)
    conn.commit()
    
create_tables("./")
