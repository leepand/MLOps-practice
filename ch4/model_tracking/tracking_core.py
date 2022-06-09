import time
import sqlite3
import os

current_path = "./"

class ModelTrack(object):

    """
    :param nick_name:        str，用户名，多人使用下可起到数据隔离。
    :param project_name:     str，项目名称。
    :param project_remark:   str，项目备注，默认为空。
    项目名称如不存在会新建
    """
    def __init__(self, task_name, task_desc=''):

        self.conn = sqlite3.connect(os.path.join(current_path, 'model_track_center.db'))

        self.task_name = task_name
        self.task_desc = task_desc
        self.is_add_track = True
        self.param_dict = {}

    def _execute_sql(self,sql,values=None):
        self.conn.execute(sql, values)
        self.conn.commit()

    # 检查model_name是否重复
    def _check_model_name(self, model_name, model_count, task_id):
        if model_name == '':
            model_name = self.task_name + '_' + str(model_count + 1)

        else:
            # 判断是否有model_name
            if self._is_exist_model_name(model_name, task_id):
                model_name = model_name + '_' + str(model_count + 1)
            else:
                model_name = self.model_name

        if self._is_exist_model_name(model_name, task_id):
            return self._check_model_name(model_name, model_count, task_id)
        else:
            return model_name

    # 检查Task name 是否存在
    def _is_exist_task_name(self, task_name):

        sql = "select 1 from model_task m where m.task_name = '%s'"%task_name
        task_table = self.conn.execute(sql).fetchall()

        if len(task_table) != 0:
            return True
        else:
            return False

    # 检查model name 是否存在
    def _is_exist_model_name(self, model_name, task_id):

        sql = "select 1 from model_track  mt where mt.task_id = %d and mt.model_name = '%s'" % (task_id, model_name)
        model_table = self.conn.execute(sql).fetchall()

        if len(model_table) != 0:
            return True
        else:
            return False

    def log_param(self, param_dict, param_type):
        self.param_dict[param_type] = param_dict

    def log_model_name(self, model_name):
        self.model_name = model_name

    def log_model_desc(self, model_desc):
        self.model_desc = model_desc

    def log_metric(self, metric_name, metric_value, epoch, is_best=0):

        if self.is_add_track:
            self._add_track_logs()
            self.is_add_track = False
        
        sql = """insert 
                 into 
                    model_metric 
                    (model_id, metric_name, metric_type, epoch, metric_value, is_best) 
                 values (?, ?, ?, ?, ?, ?)"""
        self._execute_sql(sql, (self.model_id, metric_name,"line", epoch, '%.4f'%(metric_value), is_best))
        
    def log_best_result(self, best_name, best_value, best_epoch):
        sql = "insert into best_result () values (null, ?, ?, ?, ?, ?)"
        self._execute_sql(sql, (self.sub_model_id, best_name, '%.4f' % (best_value), best_epoch, create_time))
        

    # 添加模型超参数及其他元数据
    def _add_track_logs(self):

        # 插入model
        if not self._is_exist_task_name(self.task_name):
            sql = "insert into model_task (task_name,task_description) values (?, ?)"
            self._execute_sql(sql, (self.task_name, self.task_desc))

        sql = "select task_id from model_task m where m.task_name = '%s'"%self.task_name
        task_id = self.conn.execute(sql).fetchall()[0][0]

        sql = "select count(1) from model_track sm where sm.task_id = %d"%task_id
        model_count = self.conn.execute(sql).fetchall()[0][0]

        # 插入sub model
        model_name = self._check_model_name(self.model_name, model_count, task_id)
        sql = "insert into model_track (task_id,model_sequence,model_name,model_description) values (?, ?, ?, ?)"
        self._execute_sql(sql, (task_id, model_count + 1, model_name, self.model_desc))

        sql = "select model_id from model_track sm where sm.task_id = ? and sm.model_name = ?"
        self.model_id = self.conn.execute(sql, (task_id, model_name)).fetchall()[0][0]
        print(self.model_id,model_name,"self.model_id")
        # 插入model params
        for param_type, value in self.param_dict.items():

            for param_name, param_value in value.items():
                sql = "insert into model_params (model_id, param_type, param_name, param_value) values (?, ?, ?, ?)"
                self._execute_sql(sql, (self.model_id, param_type, param_name, str(param_value)))
                
    def close(self):
        self.conn.close()
