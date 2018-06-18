FROM ubuntu:16.04

MAINTAINER FIWARE Identity Manager Team. DIT-UPM

WORKDIR /opt

# Install Ubuntu dependencies
RUN apt-get update && \
    apt-get install build-essential debconf-utils ca-certificates curl git netcat -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install email dependency
RUN apt-get update && \
    echo "postfix postfix/mailname string noreply@localhost" | debconf-set-selections && \
    echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections && \
    apt-get install -y mailutils

# Configure mail
RUN sed -i 's/inet_interfaces = all/inet_interfaces = loopback-only/g' /etc/postfix/main.cf

# Install PPA
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Download latest version of the code and install npm dependencies
RUN git clone https://github.com/ging/fiware-idm.git && \
    cd fiware-idm && \
    npm cache clean -f && \
    npm install

# Change Workdir
WORKDIR /opt/fiware-idm

# Copy config file
COPY files/config.js /opt/fiware-idm/config.js
COPY files/app.js /opt/fiware-idm/app.js

# Create certificates for https
RUN mkdir certs && \
    openssl genrsa -out idm-2018-key.pem 2048 && \
    openssl req -new -sha256 -key idm-2018-key.pem -out idm-2018-csr.pem -batch && \
    openssl x509 -req -in idm-2018-csr.pem -signkey idm-2018-key.pem -out idm-2018-cert.pem && \
    mv idm-2018-key.pem idm-2018-cert.pem idm-2018-csr.pem certs/

# Copy config database file
COPY files/config_database.js extras/docker/config_database.js

# Run Idm Keyrock
COPY files/docker-entrypoint.sh /opt/fiware-idm/docker-entrypoint.sh
RUN chmod 755 docker-entrypoint.sh

ENTRYPOINT ["/opt/fiware-idm/docker-entrypoint.sh"]
