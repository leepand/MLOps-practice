import pandas as pd
conn = sqlite3.connect(os.path.join(model_registry_path, 'model_registry_center.db'))
pd.read_sql_query("SELECT * FROM model_registry;", conn)
