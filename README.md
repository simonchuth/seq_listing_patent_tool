# Tools for generating sequence listing for patent application

## Work in progress

## Introduction

This tool is designed to generate a sequence listing in the format prescribed by WIPO Standard ST.25. The user can use the template csv file to upload multiple sequences to the app to generate the sequence listing. 

## Installation

0. If you do not have git, please following the instruction [here][1] to install git. And refer to [this page][2] to install python 3.7 if you do not have it.
1. Use git to clone this repository
```
git clone https://github.com/simonchuth/seq_listing_patent_tool.git
```
2. Use pip to install the required dependencies
```
pip install --upgrade -r requirements.txt
```
3. Use the following command to run the streamlit app
```
streamlit run src/app.py
```

### Running on AWS EC2 instance
Use the `iptables` to redirect the traffic from port 80 to port 8501 (before running the streamlit app)
```
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8501
```





<!-- Reference links -->
[1]: https://git-scm.com/downloads
[2]: https://www.python.org/downloads/