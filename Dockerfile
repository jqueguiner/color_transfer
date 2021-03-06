FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --fix-missing

RUN apt-get install -y wget python3 python3-pip build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev tzdata python-opencv && \
        dpkg-reconfigure --frontend noninteractive tzdata


RUN mkdir -p /src

WORKDIR /src

COPY requirements.txt /src/requirements.txt
COPY example.ipynb /src/example.ipynb
COPY color_transfer /src/color_transfer
COPY images /src/images
COPY run_notebook.sh /src/run_notebook.sh
COPY set_password.py /src/set_password.py

RUN pip3 install -r requirements.txt
RUN pip3 install jupyter

EXPOSE 8888

ENTRYPOINT ["sh", "/src/run_notebook.sh"]
