#FROM ubuntu:18.04
FROM kalilinux/kali-rolling

ENV LANG C.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL C.UTF-8  
CMD locale-gen
ENV TERM xterm-256color

#RUN adduser -D yavs-api
RUN apt update && apt full-upgrade -y
RUN apt install -y python3-flask iputils-ping nmap
RUN apt install python3 python3-pip nmap python python-pip git exploitdb -y


COPY . /root/yavs
RUN cd /root/yavs
#RUN chmod +x boot.sh

WORKDIR /root/yavs
RUN /root/yavs/install.sh

ENV FLASK_APP app.py

#RUN chown -R yavs-api:yavs-api ./
#USER yavs-api

RUN searchsploit -t MySQL 5.0 --colour

EXPOSE 8000
CMD ["/bin/bash", "-c", "pwd"]
CMD ["/bin/bash", "-c", "gunicorn --bind=0.0.0.0:8000 app:app"]