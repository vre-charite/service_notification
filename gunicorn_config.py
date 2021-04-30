# gunicorn_config.py
workers = 4
threads = 2
bind = '0.0.0.0:5065'
daemon = 'false'
worker_connections = 5
accesslog = 'access.log'
errorlog = 'error.log'
loglevel = 'info'

