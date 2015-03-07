FROM planout/base_django:2.7
MAINTAINER pdt <pdthanh06@gmail.com>

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
