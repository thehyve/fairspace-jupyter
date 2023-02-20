# Local development

You can run the docker images locally for testing.

## Run jupyterhub-singleuser

### Configure and run

Create `.env` file:

For connecting to a local development instance:
```shell
KEYCLOAK_SERVER_URL=http://localhost:5100
KEYCLOAK_REALM=fairspace
KEYCLOAK_USERNAME=user
KEYCLOAK_PASSWORD=fairspace123
    
TARGET_URL=http://172.17.0.1:8080
REALM_URL=http://172.17.0.1:5100/auth/realms/fairspace
CLIENT_ID=workspace-client
CLIENT_SECRET=**********
REFRESH_TOKEN=...

JUPYTER_COMMAND=jupyter-notebook
```

In order to mount files exported from Fairspace to extra storage for further analysis in JupyterHub, include `ANALYSIS_EXPORT_TARGET` variable
as a unique Fairspace extra storage root collection (same as used in Fairspace configuration):
```shell
ANALYSIS_EXPORT_TARGET=analysis-exports
```

To mount external storages that are configured in Fairspace, include `EXTERNAL_TARGETS` variable
as a comma-separated list of unique storage names (same as used in Fairspace configuration):
```shell
EXTERNAL_TARGETS=test
```

Fetch refresh token:

```shell
source .env
curl -s -d "client_id=${CLIENT_ID}" -d "client_secret=${CLIENT_SECRET}" -d "username=${KEYCLOAK_USERNAME}" -d "password=${KEYCLOAK_PASSWORD}" -d 'grant_type=password' -d 'scope=offline_access' "${KEYCLOAK_SERVER_URL}/auth/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" | jq -r '.refresh_token'
```

Update the `REFRESH_TOKEN` variable in the `.env` file.

#### Build images
```shell
docker build ../projects/jupyterhub-singleuser -t jupyterhub-singleuser-local:latest
docker build ../projects/jupyterhub-hub -t jupyterhub-hub-local:latest
```

#### Run singleuser image

```shell
# Run Jupyter notebook
docker run --name jupyter-dev --rm -it --env-file .env -p 8888:8888 --privileged jupyterhub-singleuser-local:latest /start
```

#### Run Jupyter Hub using minikube

Please check the [deploy.sh](hub/deploy.sh) script.
It assumes Helm3 to be available in `~/bin/helm3/helm` and
Keycloak to be running at http://localhost:5100.

The ingress node will listen to http://jupyterhub.local, so make sure to
- add `$(minikube ip) jupyterhub.local` to `/etc/hosts`:
  ```shell
  echo "$(minikube ip) jupyterhub.local" >> /etc/hosts
  ```
- add `http://jupyterhub.local/*` to _Valid Redirect URIs_ in Keycloak.

To start Jupyter Hub:
```shell
# Start minikube
minikube start
```
---
**NOTE**

To run use **containerd** instead of **docker** as CRI runtime,
use `--container-runtime=containerd` property for the start command
and change the `container_runtime` property in `./hub/deploy.sh` to "containerd".


---
```
minikube addons enable ingress

# Open kubernetes dashboard
minikube dashboard

# Push images to minikube repository and start Jupyter Hub
./hub/deploy.sh
```
The script creates the `jupyterhub-dev` namespace where all other objects are created.

To shutdown Jupyter Hub, use one of the following:
```shell
# Uninstall Jupyter Hub using Helm
helm uninstall jupyterhub-local -n jupyterhub-dev
# Delete jupyterhub-dev namespace
kubectl delete ns jupyterhub-dev
```
