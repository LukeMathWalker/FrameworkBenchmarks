import multiprocessing
import os
import sys

_is_pypy = hasattr(sys, "pypy_version_info")
_is_travis = os.environ.get("TRAVIS") == "true"

workers = int(multiprocessing.cpu_count() * 1.5)
if _is_travis:
    workers = 2

bind = "0.0.0.0:8080"
keepalive = 120
errorlog = "-"
pidfile = "gunicorn.pid"

if _is_pypy:
    worker_class = "sync"
else:
    worker_class = "meinheld.gmeinheld.MeinheldWorker"

    def post_fork(server, worker):
        import meinheld
        import meinheld.server
        import meinheld.patch
        meinheld.server.set_access_logger(None)
        meinheld.set_keepalive(keepalive)
        meinheld.patch.patch_all()
