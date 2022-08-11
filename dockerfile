FROM python:latest
LABEL curator="tuanha"

WORKDIR /usr/app/src

COPY ./ ./

RUN apt-get update && \
	apt-get upgrade -y && \
    apt-get install -y -f gstreamer-1.0 && \
    apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 libgstreamer1.0-0 gstreamer1.0-plugins-{base,good,bad,ugly} gstreamer1.0-tools python3-gi gir1.2-gstreamer-1.0 -y && \
    pip3 install pycairo && \
    pip3 install PyGObject && \
    python -m pip install -r dependencies.txt --user

CMD ["python", "./record.py"]