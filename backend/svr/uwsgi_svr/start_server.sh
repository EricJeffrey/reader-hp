# !/bin/bash
nohup uwsgi --http 0.0.0.0:8686 --static-map /static=../static/  --wsgi-file ./run.py &
