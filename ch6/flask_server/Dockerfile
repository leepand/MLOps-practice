# 在Python 3.7下使用基础镜像
FROM python:3.7
 
# 设置我们的工作目录为app
WORKDIR /app 
 
# 安装Python软件包Pandas、Scikit-Learn和uWSGI
RUN pip install pandas scikit-learn flask uwsgi
 
# 复制模型目录和server.py文件
ADD ./models ./models
ADD server.py server.py
 
# 从容器中暴露出5000端口
EXPOSE 5000
 
# 启动Nginx及Python应用程序
CMD service nginx start && uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=server:app
