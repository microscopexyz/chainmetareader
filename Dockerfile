FROM python:3.9-slim
#RUN mkdir /opt
WORKDIR /opt/
EXPOSE 8081
COPY [".", "/opt/"]
RUN   pip3 install -i https://mirrors.aliyun.com/pypi/simple/  -r requirements.txt
#CMD   uvicorn server:app --port 8081 --host 0.0.0.0
CMD python3 -u server.py