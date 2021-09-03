# 进程数
workers = 2
# 每个进程的线程数
threads = 4
# 端口5000
bind = '0.0.0.0:8040'
# 工作模式协程
worker_class = 'gevent'
# 最大并发量
worker_connections = 100
# 进程pid文件
pidfile = 'gunicorn.pid'
# 访问日志和错误信息日志的路径
# 日志记录级别
loglevel = 'info'
# 代码发生变化是否自动重启
reload = True