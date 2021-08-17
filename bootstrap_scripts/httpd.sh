#!/bin/bash -xe
sudo yum install httpd
sudo chkconfig httpd on
sudo service httpd start
