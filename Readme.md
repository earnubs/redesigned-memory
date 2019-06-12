# Front End Test

Foreign exchange trade app

# Requirements

To run this project you need to install `docker` and
`docker-composer`.

[Docker install instructions](https://docs.docker.com/install/):
[Docker-compose install instructions](https://docs.docker.com/compose/install/):

Optionally you need to install GNU Make to use the utility Makefiles
inside each service folder.

# How to run it

At the root of the project run:

```
./scripts/start
```

This will build/download images and bring up all services. Once
started, visit the UI at `http://localhost:3000`.

You can check the startup state with `docker-compose logs -f`.

Finally a convenience script stop all containers is also provided:

```
./scripts/stop
```
# Important URLs

- UI: `http://localhost:3000`
- API root: `http://localhost:3000/api/`
- API docs: `http://localhost:3000/api/docs/`

# Structure

The project is split in two main parts, the first one is the `backend`
which serves the API endpoints and the other must be the `frontend`.

## Development environment details

The `frontend` container must run at `http://localhost:3000` proxies
requests under `/api` to the `backend`.

