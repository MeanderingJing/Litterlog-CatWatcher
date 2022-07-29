# Cat Data Schema

Repository containing the cat data schema for data storage and visualization using sqlalchemy, alembic, and postgresql

## building

You can build the kernel.test.schema docker by running build.sh
    ./build.sh
this will build a container with tag `test_station_watcher:latest`

to interact with the container, use
    docker run -it --name watcher test_station_watcher:latest /bin/bash

### Notes (running on WSL:Ubuntu)

From the kernel.test.schema directory

    pip install -e .

Installing postgresql (needs to be done before installing pyscopg2)

    sudo apt install postgresql postgresql-contrib
    sudo service postgresql start
    sudo service postgresql status
    sudo apt install libpq-dev

Install pyscopg2

    pip install psycopg2

Generating new migrations
./alembic.sh revision --autogenerate -m "myfirstmigration"

## Deploying to Production

### Prod environment

We deploy onto our on-site `util` server using the docker/docker-compose.yml via a service at `/etc/systemd/system/test_station.service`.

Only the test_station_watcher service depends on kernel.test.schema, the other services are pulled from external registries.

### Deploy updated kernel.test.schema

Deploying is manual right now, you should clone this repo onto util to build the watcher container:

    ```bash
    cd path/to/test-station-schema/kernel.test.schema
    docker build . -t registry.kernel.corp/software/test_station_watcher:latest -f docker/Dockerfile
    docker login registry.kernel.corp
    docker image push registry.kernel.corp/software/test_station_watcher:latest
    ```

Then restart the watcher service

    ```bash
    systemctl restart test_station.service
    ```

### Migrate db in prod

After deploying the latest container, if you need to run alembic migrations:

    ```bash
    docker exec -it test_station_watcher_1 /bin/bash
    # inside bash
    kts-migrate
    ```
