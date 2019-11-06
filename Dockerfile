FROM docker.io/python
MAINTAINER meisanggou


ADD https://raw.githubusercontent.com/zhmsg/dms/master/requirement.txt /tmp/
RUN pip install -r /tmp/requirement.txt

ENV DMSPATH /opt/dms
ENV PYTHONPATH $DMSPATH

CMD ["gunicorn", "-b", "0.0.0.0:2000", "-w", "4", "-k", "gevent", "--chdir", "$DMSPATH/Web", "msg_web:msg_web"]