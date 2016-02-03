cd Web
# nohup python msg_web.py 1>> msg_web.log 2>>msg_web.log &
nohup gunicorn -c gunicorn.conf msg_web:msg_web 1>>msg_web.log 2>>msg_web.log &