import os
import sqlite3
import pandas as pd
import re


column_re = re.compile('(.+?)\((.+)\)', re.S)
column_split_re = re.compile(r'(?:[^,(]|\([^)]*\))+')

def _format_create_table(sql):
    create_table, column_list = column_re.search(sql).groups()
    columns = ['  %s' % column.strip()
               for column in column_split_re.findall(column_list)
               if column.strip()]
    return '%s (\n%s\n)' % (
        create_table,
        ',\n'.join(columns))

def format_create_table(sql):
    try:
        return _format_create_table(sql)
    except:
        return sql

sql = """drop table if exists model_registry;
create table model_registry
(
    id INTEGER PRIMARY KEY ASC,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    registered_date TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    remote_path TEXT NOT NULL,
    stage TEXT DEFAULT 'DEVELOPMENT' NOT NULL
);"""



model_registry_path = "./"

class ModelRegistry:
    def __init__(self, table_name='model_registry'):
        self.conn = sqlite3.connect(os.path.join(model_registry_path, 'model_registry_center.db'))
        self.table_name = table_name

    def deploy_model(self, model, model_name, version = 1):
        model_path = '/models/{}_v{}'.format(model_name, version)
        values = (model_name, version, model_path)
        sql = "insert into {} (name, version, remote_path) values (?, ?, ?)".format(self.table_name)
        #task.push_model(model, model_path)
        self._execute_sql(sql, values)

    def query_registry_info(self):
        sql = "select * from {} limit 10".format(self.table_name)
        query_results = self.conn.execute(sql).fetchall()
        return query_results

    def update_stage(self, model_name, version, stage):
        sql = "update {} set stage = ? where name = ? and version = ?;".format(self.table_name)
        self._execute_sql(sql, (stage, model_name, version))

    def update_version(self, model, model_name):
        version_query = """select 
                                version 
                            from 
                                {} 
                            where
                                name = '{}' 
                            order by 
                                registered_date 
                            desc limit 1
                            ;""".format(self.table_name, model_name)
        version = pd.read_sql_query(version_query, self.conn)
        version = int(version.iloc[0]['version'])
        new_version = version + 1
        remote_path = '/models/{}_v{}'.format(model_name, new_version)
        #task.push_model(model, remote_path)
        self.deploy_model("model",model_name, new_version)
    def get_production_model(self, model_name):
        sql = """
                select
                    *
                from
                    {}
                where
                    name = '{}' and
                    stage = 'PRODUCTION'
                ;""".format(self.table_name, model_name)
        return pd.read_sql_query(sql, self.conn)
    def init_db(self, sql_script):
        self.conn.executescript(sql_script)
        self.conn.commit()

    def _execute_sql(self, sql, values=None):
        self.conn.execute(sql, values)
        self.conn.commit()

    def close(self):
        self.conn.close()

sql_script = format_create_table(sql)
registry_init = ModelRegistry()
registry_init.init_db(sql_script)
registry_init.deploy_model("model","churn_first_model")
registry_init.update_version("model","churn_first_model")
registry_init.update_stage(model_name = "churn_first_model", version='2', stage="PRODUCTION")
