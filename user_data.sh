#!/bin/bash
yum update -y
yum install -y python3
yum install -y git
pip3 install --upgrade -r requirements.txt

git clone https://github.com/simonchuth/seq_listing_patent_tool.git /home/ec2-user
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8501
streamlit run /seq_listing_patent_tool/src/app.py