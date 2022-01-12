FROM python:3.8.5

# OpenCV
RUN apt-get update && \
    apt-get install -y libxml2-dev && \
    apt-get install -y libsm6 && \
    apt-get install -y libxext6 && \
    apt-get install -y ffmpeg && \
    apt-get install -y vim && \
    apt-get install -y openvpn && \
    apt-get install -y openconnect


COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir /generated_badges

COPY . .

# TODO: Replace lines below with python main.py when it doesn't need VPN to run
RUN chmod +x run.sh
CMD ./run.sh