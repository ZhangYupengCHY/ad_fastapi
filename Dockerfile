FROM python:3.7
WORKDIR /fastapi
COPY requirements.txt ./
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
EXPOSE 8010
CMD ["python","main.py"]

