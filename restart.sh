sh stop_web.sh
find -name "*.log" | xargs rm -rf
git stash
git pull
sh start_web.sh