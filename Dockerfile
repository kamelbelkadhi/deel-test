FROM postgres:latest

# install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get -y install python3
RUN apt-get -y install postgresql-server-dev-10 gcc python3 musl-dev

# install psycopg2 and pandas library with PIP
RUN pip3 install psycopg2 pandas

# add the 'postgres' admin role
USER postgres

# expose Postgres port
EXPOSE 5432

# bind mount Postgres volumes for persistent data
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
