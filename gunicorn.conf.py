# bind = "unix:/tmp/gunicorn.sock"   #绑定的ip与端口

bind = "0.0.0.0:8080"   #绑定的ip与端口

backlog = 512                #监听队列数量，64-2048
chdir = '/home/baird/orderlunchEnv/OrderLunch'  #gunicorn要切换到的目的工作目录

worker_class = 'sync' #使用gevent模式，还可以使用sync 模式，默认的是sync模式
workers = 4
threads = 8

loglevel = 'info' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别>无法设置

access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s'

accesslog = "./gunicorn_access.log"      #访问日志文件
errorlog = "./gunicorn_error.log"        #错误日志文件
# accesslog = "-"  #访问日志文件，"-" 表示标准输出
# errorlog = "-"   #错误日志文件，"-" 表示标准输出





