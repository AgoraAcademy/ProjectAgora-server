FROM ubuntu

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get -f install -y nginx python3.6
ADD default /etc/nginx/sites-available
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 10081