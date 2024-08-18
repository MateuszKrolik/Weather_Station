sudo docker run --name some-mysql \
  -p 3306:3306 \
  -v /my/own/datadir:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -d mysql