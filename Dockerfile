FROM ubuntu

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get -f install -y nginx python3.6 python3-pip
RUN timedatectl set-timezone Asia/Shanghai
ADD default /etc/nginx/sites-available

EXPOSE 10081