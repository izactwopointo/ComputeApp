#!/bin/bash -xe

# version: 31Aug

#!/bin/bash
sudo yum update -y
sudo yum -y install httpd php mysql
sudo chkconfig httpd on
sudo service httpd start
echo "Hello Nigga from $(hostname -f)" > /var/www/html/index.html
sudo yum install -y mysql57 curl

# Ping github
curl "https://github.com/miztiik"

# To Connect to DB
# mysql -u {User_name} -p -h {RDS_End_Point} {DB_NAME}
