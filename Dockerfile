FROM ubuntu

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get -f install -y nginx python3.6 python3-pip
ADD default /etc/nginx/sites-available
RUN ls
RUN pip3 install --no-cache-dir -r /var/jenkins_home/workspace/ProjectAgora-server/requirements.txt

EXPOSE 10081