## Docker Set Up 

Sources:
* https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu
* https://techexpert.tips/postgresql/postgresql-docker-installation/
* https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

Install Docker:
```
sudo apt-get remove docker docker-engine docker.io
sudo apt install docker.io
sudo snap install docker
docker --version

sudo apt-get install docker.io


#To set up a user and user docker without sudo 
sudo usermod -aG docker ${USER}
```
Then EXIT and enter the system 


To install postgres image:
```
docker pull postgres
```

List all Docker Images:
```
docker images
```

Create folder for volumes of postgres:
```
#!!Create volumes of postgres in empty table 
mkdir -p docker/postgres/volumes
```

Create and Run container:
```
docker run --name postgresqlLYS -e POSTGRES_USER=ubuntu -e POSTGRES_PASSWORD=ubuntu -p 5432:5432 -v /home/ubuntu/lightyear/docker/postgres/volumes:/var/lib/postgresql/data -d postgres
```
--name <name_of_container>
-d <image>  — in detached mode
-v /<localpath>:/var/lib/postgresql/data


See Active and Inactive Containers:
```
docker ps
docker ps -a 
```


### Connecting to PostgreSQL
Connect to container using its name:
```
docker exec -ti postgresqlLYS /bin/bash
```
-ti — in foreground

Inside of Container to connect to Postgres using Username:
```
psql -U ubuntu -W
```
-W — to enter password
-U <username>

Inside of Postgres:
\q   — to quit
\l   - List of databases
\dn  - List of Schemas under current db
\c <database name>; — connect to specific database and enter a password for the user

Postgres SQL Connection:
```
POSTGRES_DATABASE_URI = 'postgresql+psycopg2://ubuntu:ubuntu@0.0.0.0:5432/haros_db'
```
Example: `postgres://user:secret@localhost:5432/DB_NAME`


### Installing psycopg2

To get location of path for psycopg2
```
pg_config --bindir
```

Add the result of above operation before `:$PATH`:
```
export PATH=/usr/lib/postgresql/12/bin/:$PATH
```

```
sudo python3 -m pip install psycopg2
```