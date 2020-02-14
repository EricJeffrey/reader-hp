# !/bin/bash
echo -e "copy html and js files? (Y/N) \c"
read a
if [[ $a == 'y' || $a == 'Y' ]]; then
    cp /home/yu/sjf/reader-hp/backend/svr/static/*.html /home/yu/sjf/webapp_reader/svr/static/
    cp /home/yu/sjf/reader-hp/backend/svr/static/common.js /home/yu/sjf/webapp_reader/svr/static/
fi
echo -e "change to webapp_reader/svr/uwsgi ans start server? (Y/N) \c"
read a
if [[ $a == 'y' || $a == 'Y' ]]; then
    cd /home/yu/sjf/webapp_reader/svr/uwsgi_svr/
    echo -e "start with nohup &?(Y/N) \c"
    read a
    if [[ $a == 'y' || $a == 'Y' ]]; then
        nohup uwsgi --socket 127.0.0.1:4399 --static-map /reader/static=../static/  --wsgi-file ./run.py &
    else 
        uwsgi --socket 127.0.0.1:4399 --static-map /reader/static=../static/  --wsgi-file ./run.py
    fi
fi


