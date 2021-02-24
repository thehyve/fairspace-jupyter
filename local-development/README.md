# Local development

You can run the docker images locally for testing.

## Run jupyterhub-singleuser

### Fetch refresh token

```shell
KEYCLOAK_SERVER_URL=https://keycloak.ci.fairway.app \
KEYCLOAK_REALM=ci \
KEYCLOAK_CLIENT_ID=fairspace-ci-private \
KEYCLOAK_CLIENT_SECRET=4c4e5e3b-a6ed-45fd-a394-46c4f5eea510 \
KEYCLOAK_USERNAME=user \
KEYCLOAK_PASSWORD=fairspace123 \
curl -s -d "client_id=${KEYCLOAK_CLIENT_ID}" -d "client_secret=${KEYCLOAK_CLIENT_SECRET}" -d "username=${KEYCLOAK_USERNAME}" -d "password=${KEYCLOAK_PASSWORD}" -d 'grant_type=password' -d 'scope=offline_access' "${KEYCLOAK_SERVER_URL}/auth/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" | jq -r '.refresh_token'
```
### Configure and run

Create `.env` file:
```shell
TARGET_URL=https://fairspace.ci.fairway.app/api/webdav
REALM_URL=https://keycloak.ci.fairway.app/auth/realms/ci
CLIENT_ID=fairspace-ci-private
CLIENT_SECRET=4c4e5e3b-a6ed-45fd-a394-46c4f5eea510
REFRESH_TOKEN=...

JUPYTER_COMMAND=jupyter-notebook
```

#### Build image
```shell
docker build ../projects/jupyterhub-singleuser -t jupyter-local:latest
```

#### Run image

```shell
docker run --name jupyter-dev --rm -it --env-file .env -p 8888:8888 --privileged jupyter-local:latest /start
```

## Mount external storages

To mount external storage, together with the storage configured as a target, update a `targets.json` file:

```json
[
  {
    "name": "fairspace_test",
    "url": "https://fairspace.test.fairway.app/api/webdav"
  }
]

```
