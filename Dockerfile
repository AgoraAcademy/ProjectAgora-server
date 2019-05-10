FROM ubuntu:18.04

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y tzdata
RUN ln -sf /usr/share/zoneinfo/Asia/ShangHai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get -f install -y nginx python3.6 python3-pip
ADD default /etc/nginx/sites-available

EXPOSE 10081