import ebonite
from ebonite import Ebonite, create_model
from ebonite.runtime import run_model_server
from ebonite.ext.flask.server import FlaskServer

dep_client = Ebonite.custom_client('sqlalchemy', 'local',
                                   meta_kwargs={'db_uri': 'sqlite:///mlops_meta.db'},
                                   artifact_kwargs={'path': './artifact'})

task = dep_client.get_or_create_task('Model-deploy', 'Model-task')

model = ebonite.create_model(run_my_model, df, 'lr_model_1')

#  persist model
task.push_model(model)


run_model_server(model, FlaskServer())
