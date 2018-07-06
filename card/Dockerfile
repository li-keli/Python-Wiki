FROM ubuntu:16.04

WORKDIR /home/work

COPY . .

RUN apt-get update -y && \
apt-get install tesseract-ocr python3-pip python3-tk -y && \
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ && \
apt-get clean && rm -rf /var/lib/apt/lists/* && \
cp config/digits /usr/share/tesseract-ocr/tessdata/configs/digits

EXPOSE 5000

CMD python3 web.py
