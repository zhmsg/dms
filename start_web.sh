# python c_file.py

cd Table
python develop_table.py

if [ -d "/jy_static/dms_static" ];then
    cp -r ../Web/static2/* /jy_static/dms_static
fi

cd ../Web
nohup gunicorn -c gunicorn.conf msg_web:msg_web 1>>msg_web.log 2>>msg_web.log &
nohup python tornado_app.py 1>>tornado_app.log 2>>tornado_app.log &