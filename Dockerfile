FROM docker.io/centos
MAINTAINER meisanggou

RUN yum install -y gcc unzip wget
RUN yum install -y python-devel mysql-devel

# install setuptools
RUN curl -o /tmp/setuptools.zip https://pypi.python.org/packages/a9/23/720c7558ba6ad3e0f5ad01e0d6ea2288b486da32f053c73e259f7c392042/setuptools-36.0.1.zip#md5=430eb106788183eefe9f444a300007f0
RUN unzip /tmp/setuptools.zip -d /tmp

RUN cd /tmp/setuptools-36.0.1/ && python setup.py install && rm -rf /tmp/setuptools*

# install pip
RUN curl -o /tmp/pip-9.0.1.tar.gz https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da33009719497f01a4ba69d63c9
RUN tar -zxvf /tmp/pip-9.0.1.tar.gz -C /tmp

RUN cd /tmp/pip-9.0.1 && python setup.py install && rm -rf /tmp/pip*

# install python package
RUN pip install gunicorn
RUN pip install gevent
RUN pip install Flask
RUN pip install Flask-Login
RUN pip install MySQL-python
RUN pip install requests
RUN pip install xlwt
RUN pip install Flask-APScheduler
RUN pip install redis
RUN pip install JYAliYun
RUN pip install Fabric
RUN pip install m2crypto
RUN pip install JYTools
