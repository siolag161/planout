FROM tutum.co/planout/python:2.7
MAINTAINER pdt <pdthanh06@gmail.com>

################################ install node
RUN \
  cd /tmp && \
  wget http://nodejs.org/dist/node-latest.tar.gz && \
  tar xvzf node-latest.tar.gz && \
  rm -f node-latest.tar.gz && \
  cd node-v* && \
  ./configure && \
  CXX="g++ -Wno-unused-local-typedefs" make && \
  CXX="g++ -Wno-unused-local-typedefs" make install && \
  cd /tmp && \
  rm -rf /tmp/node-v* && \
  npm install -g npm && \
  echo -e '\n# Node.js\nexport PATH="node_modules/.bin:$PATH"' >> /root/.bashrc

################################ install node
RUN npm install -g grunt-cli
RUN npm install -g foreman

# create unprivileged user
RUN useradd -ms /bin/bash planout
RUN cd && cp -R /root/.bashrc  /root/.gitconfig /root/.scripts /root/.profile /home/planout

RUN mkdir -p /opt/planout.vn

ADD ./requirements/ /opt/planout.vn/requirements/
RUN pip install -r /opt/planout.vn/requirements/stage.txt # install prod requirements

ADD . /opt/planout.vn
RUN chown -R planout:planout /opt/planout.vn

WORKDIR /opt/planout.vn

EXPOSE 80

CMD ["true"]
