FROM python:3.9-slim
ENV PYTHONIOENCODING=utf-8
ENV CHAINMETA_DB_CONN='mysql+pymysql://CD6KPB7xM7EYsZ9.chaintool_rw:W1PkWn2hfOAy@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/chainmeta?ssl=true&ssl_ca=/etc/ssl/cert.pem'
#RUN mkdir /opt
WORKDIR /opt/
EXPOSE 8081
COPY [".", "/opt/"]
RUN   pip3 install -i https://mirrors.aliyun.com/pypi/simple/  -r requirements.txt
CMD   uvicorn server:app --port 8081 --host 0.0.0.0
#CMD python3 -u ./api_server/server.py