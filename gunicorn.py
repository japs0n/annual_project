import multiprocessing

chdir = '/var/src/flask'
bind = "0.0.0.0:8008"
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
reload = True
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "/var/src/flask/logs/gunicorn_access.log"
loglevel = 'debug'  # 错误日志等级
errorlog = "/var/src/flask/logs/gunicorn_error.log"
