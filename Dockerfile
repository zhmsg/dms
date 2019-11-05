FROM docker.io/python
MAINTAINER meisanggou


ADD https://raw.githubusercontent.com/zhmsg/dms/master/requirement.txt /tmp/
RUN pip install -r /tmp/requirement.txt
