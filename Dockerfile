FROM docker.io/centos
MAINTAINER meisanggou

RUN yum install -y gcc epel-release && yum install -y python2-pip python-devel mysql-devel

ADD https://raw.githubusercontent.com/zhmsg/dms/master/requirement.txt /tmp/
RUN pip install -r /tmp/requirement.txt
