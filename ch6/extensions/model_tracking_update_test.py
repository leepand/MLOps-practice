import datetime

exp=Experiment(db_uri='sqlite:///mlops_meta.db')
exp._create_exp(TExperiment(name="mltracking",
                            author="user",
                            sub_model_remark="churn model experiment tracking",
                            nick_name="churn_model_exp",
                            sub_model_sequence=1,
                            creation_date = datetime.datetime.utcnow(),
                            task_id=1))
