sh stop_web.sh
find -name "*.log" | xargs rm -rf
git pull
sh start_web.sh