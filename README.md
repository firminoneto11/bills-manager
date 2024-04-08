# Bills Manager

## Instructions on how to run the project

Before continuing, make sure you have both [docker](https://www.docker.com/) and
[docker compose](https://docs.docker.com/compose/) installed on your machine.

If you have the [makefile](https://makefiletutorial.com/) tool installed you can simply:

```bash
make local
```

It will spin up the project as whole using a locally simple sqlite database. In case you
don't have it installed, use these commands:

```bash
# Spins up the container in attached mode
docker compose -f ./scripts/docker-compose-local.yaml up --build

# Removes the container after its utilization
docker rm bills-manager-local
```

## Instructions on how to run the tests

Following the pattern as before, you can simply run:

```bash
# If you have the make tool installed
make test

# If you don't have it
docker compose -f ./scripts/docker-compose-test.yaml up --build
```
