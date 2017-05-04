#!/usr/bin/env bash
cd Table
python develop_table.py

if [ -d "/jy_static/dms_static" ];then
    cp -r ../Web/static2/* /jy_static/dms_static
fi

cd ../Web
# nohup gunicorn -c gunicorn.conf msg_web:msg_web 1>>msg_web.log 2>>msg_web.log &
gunicorn -b 0.0.0.0:2200 --backlog 2048 -w 2 -k gevent -t 2 -t 3600 -D --access-logfile msg_web_access.log  --error-logfile msg_web_error.log msg_web:msg_web

cd ../Web2
gunicorn -b 127.0.0.1:2300 -k tornado -D --access-logfile tornado_app_access.log --error-logfile tornado_app_error.log tornado_app:ado_app