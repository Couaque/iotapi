FROM kalilinux/kali-rolling

ENV LANG C.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL C.UTF-8  
ENV TERM xterm-256color

RUN apt update && apt full-upgrade -y
RUN apt install -y python3-flask iputils-ping nmap
RUN apt install python3 python3-pip curl nmap python git exploitdb -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py

COPY . /root/yavs
RUN cd /root/yavs

WORKDIR /root/yavs
RUN /root/yavs/install.sh

ENV FLASK_APP app.py

RUN searchsploit -t MySQL 5.0 --colour

EXPOSE 8000
CMD ["/bin/bash", "-c", "gunicorn -t 600 --bind=0.0.0.0:8000 app:app"]