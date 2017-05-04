#!/usr/bin/env bash
cd Table
python develop_table.py

if [ -d "/jy_static/dms_static" ];then
    cp -r ../Web/static2/* /jy_static/dms_static
fi

cd ../Web
nohup gunicorn -c gunicorn.conf msg_web:msg_web 1>>msg_web.log 2>>msg_web.log &

cd ../Web2
nohup gunicorn -b 127.0.0.1:2300 tornado_app:ado_app -k tornado 1>>tornado_app.log 2>>tornado_app.log &