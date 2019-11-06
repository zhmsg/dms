FROM docker.io/python
MAINTAINER meisanggou


ADD https://raw.githubusercontent.com/zhmsg/dms/master/requirement.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirement.txt

ENV DMSPATH /opt/dms
ENV PYTHONPATH $DMSPATH
ENV LISTENPORT 2200

CMD ["/bin/bash", "-c", "gunicorn -b 0.0.0.0:$LISTENPORT -w 4 -k gevent --chdir $DMSPATH/Web msg_web:msg_web"]