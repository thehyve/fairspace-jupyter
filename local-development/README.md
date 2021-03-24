# Local development

You can run the docker images locally for testing.

## Run jupyterhub-singleuser

### Configure and run

Create `.env` file:

- For connecting to CI:
    ```shell
    KEYCLOAK_SERVER_URL=https://keycloak.ci.fairway.app
    KEYCLOAK_REALM=fairspace
    KEYCLOAK_USERNAME=user
    KEYCLOAK_PASSWORD=fairspace123

    TARGET_URL=https://fairspace.ci.fairway.app/api/webdav
    REALM_URL=https://keycloak.ci.fairway.app/auth/realms/ci
    CLIENT_ID=fairspace-ci-private
    CLIENT_SECRET=4c4e5e3b-a6ed-45fd-a394-46c4f5eea510
    REFRESH_TOKEN=...
    
    JUPYTER_COMMAND=jupyter-notebook
    ```
- For connecting to a local development instance:
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

Fetch refresh token:

```shell
source .env
curl -s -d "client_id=${CLIENT_ID}" -d "client_secret=${CLIENT_SECRET}" -d "username=${KEYCLOAK_USERNAME}" -d "password=${KEYCLOAK_PASSWORD}" -d 'grant_type=password' -d 'scope=offline_access' "${KEYCLOAK_SERVER_URL}/auth/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" | jq -r '.refresh_token'
```

Update the `REFRESH_TOKEN` variable in the `.env` file.

#### Build image
```shell
docker build ../projects/jupyterhub-singleuser -t jupyter-local:latest
```

#### Run image

```shell
docker run --name jupyter-dev --rm -it --env-file .env -p 8888:8888 --privileged --volume $(pwd)/targets.json:/opt/proxy/targets.json jupyter-local:latest /start
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
