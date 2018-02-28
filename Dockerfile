FROM python:3.5.0

ADD ./medt-backend /data
WORKDIR /data

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y locales libffi-dev libssl-dev vim

RUN echo "pt_BR.UTF-8 UTF-8" > /etc/locale.gen && \
locale-gen pt_BR.UTF-8 && \
dpkg-reconfigure locales && \
/usr/sbin/update-locale LANG=pt_BR.UTF-8

RUN unlink /etc/localtime && ln -s /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

# --no-cache-dir
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# For /var/log availability
VOLUME /var/log/

# Run Migration #TODO precisa fazer remover a tabela anterior
RUN chmod +x ./run.sh

CMD ["./run.sh"]