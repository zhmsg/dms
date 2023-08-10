FROM docker.io/python
MAINTAINER meisanggou
# tag: meisanggou/dms

ADD https://raw.githubusercontent.com/zhmsg/dms/master/requirement.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirement.txt

ENV DMSPATH /opt/dms
ENV PYTHONPATH $DMSPATH
ENV LISTENPORT 2200
ENV DMS_DB_CONF_PATH /etc/dms/mysql_app.conf

ADD Dockerfile /opt/dms_Dockerfile

CMD ["/bin/bash", "-c", "gunicorn -b 0.0.0.0:$LISTENPORT -w 4 -k gevent --chdir $DMSPATH/dms/web wsgi_app:app"]
