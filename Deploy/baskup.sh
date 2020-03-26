docker exec -u root dms-mysql bash -c 'mysqldump -uzhw -p123456 dms > /root/dms.sql'
docker cp dms-mysql:/root/dms.sql .