import multiprocessing

bind = "0.0.0.0:8000"
workers = int(multiprocessing.cpu_count() * 2) + 1
worker_class = "gthread"
threads = 4
timeout = 60
graceful_timeout = 30
accesslog = "-"
errorlog = "-"
loglevel = "info"


