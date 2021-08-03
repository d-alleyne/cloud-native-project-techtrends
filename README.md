## Project TechTrends

In this project, I'm the Platform Engineer, tasked with taking an existing Flask application and applying the following practices to make it cloud native. This involves:

1) Increase the `Observability` of the application. This includes creating API endpoints to gather metrics `/metrics` as well as the status `/healthz`. Logging was also done to allow for tracing of errors.
2) Containerizing the application, which involves creating a `Dockerfile` and a `.dockerignore` (optional)
3) Creating a `Continuous Integration` pipeline using `Github Actions`. Once the `main` branch is updated, a docker image of the application is built and pushed to Container repository (Docker Hub). Ideally, automated tests should be performed prior to packaging the application, but not required for this exercise.
4) Creating Kubernetes manifests for the application. This allows the application to be deployed in a cluster, in its own namespace.
5) Using a configuration management tool (Helm) to set up different configurations of the application (e.g. sandbox, staging, production).
6) Using a `Continuous Delivery` tool (ArgoCD) to release different versions of the application.

### Changes from the base application

* Used `Python 3` for the [Docker base image](Dockerfile#L1) instead of `Python 2`. This was required as `f-strings` were used for application [logging](techtrends/app.py#L59). F-strings requires Python 3.6 or newer. See https://realpython.com/python-f-strings/
* The Vagrantfile was updated as follows:
  * OpenSUSE Leap [15.3](Vagrantfile#L15)
  * Use a different [IP](Vagrantfile#L#39) for the guest OS from the one suggested as it was unavailable.
  * Installing k3s, helm and argocd on `vagrant up` using the [shell provisioning](https://www.vagrantup.com/docs/provisioning/shell).
