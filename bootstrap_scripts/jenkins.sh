#!/bin/bash -xe
sudo apt update
sudo apt install openjdk-8-jdk -y
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
    /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins -y
sudo cp /var/lib/jenkins/secrets/initialAdminPassword /home/ubuntu/
sudo chmod 777 /home/ubuntu/initialAdminPassword
