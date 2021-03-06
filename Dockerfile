FROM planout/base-django:2.7wn
MAINTAINER pdt <pdthanh06@gmail.com>

# create unprivileged user
RUN useradd -ms /bin/bash planout
RUN cd && cp -R /root/.bashrc  /root/.gitconfig /root/.scripts /root/.profile /home/planout

RUN mkdir -p /opt/planout.vn

ADD ./requirements/ /opt/planout.vn/requirements/
RUN pip install -r /opt/planout.vn/requirements/prod.txt # install prod requirements

RUN gem install foreman
RUN npm install uglify-js -g
RUN npm install yuglify -g

ADD . /opt/planout.vn
RUN chown -R planout:planout /opt/planout.vn

WORKDIR /opt/planout.vn

EXPOSE 80

# commands
#CMD ["foreman start"]