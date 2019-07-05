# A Helm chart for Jupyter on Fairspace
This helm chart will install and setup JupyterHub to be working with a Fairspace workspace.

The connection to the workspace should be configured in the `values.yaml` file.

## Prerequisites

Install [the Google Cloud SDK](https://cloud.google.com/sdk/install), ensure
that your Google account has access to the fairspace-207108 GCP project,
log in using `gcloud auth login`, and configure Docker for access to the GCP
registries using `gcloud auth configure-docker`.

A working instance of a fairspace workspace should be setup. Relevant parameters must be 
used for configuration of JupyterHub.

## How to install

### On GCP/GKE

First create a configuration file with settings for the workspace to install. For example:

```yaml
ingress:
    domain: jupyter.mydomain.com
    
# Additional jupyter-specific variables 
```

Then use the procedure at <https://wiki.thehyve.nl/display/VRE/Deploying+Fairspace+on+GCP>
for deploying the application.

### On Minikube

By default, on minikube one would want to run the system without TLS and ingresses. An example
configuration file would be something like:

```yaml
ingress:
    enabled: false
    
# Additional jupyter-specific variables
```

We currently don't have a tested script for Minikube deployments. The steps should largely be
the same as the ones for GCP, except for configuration of GCP-specific resources, and cert-manager
installation.

#### Ingress parameters
| Parameter  | Description  | Default |
|---|---|---|
| `ingress.enabled`  | Whether or not an ingress is setup for Jupyter. Should be set to false when running locally.  | true |
| `ingress.domain`   | Domain that is used for setting up the workspace. Is used as postfix for the hostname for the specific components. For example setting `fairspace.app` as domain will setup jupyterhub at `jupyterhub.fairspace.app`  | workspace.ci.test.fairdev.app  |
| `ingress.tls.enabled`  | Whether or not an TLS is enabled on the ingresses for workspace  | true  |
| `ingress.tls.secretNameOverride`  | If set, this secret name is used for loading certificates for TLS. | `tls-<release name>` |
| `ingress.tls.certificate.obtain`  | If set, a `Certificate` object will be created, such that [cert-manager](https://cert-manager.readthedocs.io/en/latest/) will request a certificate automatically. | true |

#### Pluto parameters
| Parameter  | Description  | Default |
|---|---|---|
| `pluto.keycloak.baseUrl` | Base url of the keycloak installation, with scheme, without /auth. For example: `https://keycloak.hyperspace.fairspace.app`  |   |
| `pluto.keycloak.realm`   | Keycloak realm that is used for this hyperspace.  |   |
| `pluto.keycloak.redirectAfterLogoutUrl`   | URL to redirect the user to after logging out  |   |

#### Tool configuration
Configuration settings for specific applications should be put under a corresponding section in config.yaml:

* Jupyterhub
Settings for Jupyterhub should be in the section `jupyterhub`.
See [the Jupyterhub docs](http://zero-to-jupyterhub.readthedocs.io/en/latest/user-environment.html) for more information on the specific settings

## Image pull secrets
When pulling docker images from a private repository, k8s needs credentials to do so. This can be configured using [image pull secrets](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry).
To use the secret for installing a workspace, follow these steps:
- Add [credentials for jupyterhub](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/jupyterhub/values.yaml#L55) separately:
  ```yaml
    jupyterhub:
      hub:
        imagePullSecret:
          enabled: true
          registry: eu.gcr.io
          username: ...
          email: ...
          password: ...
      singleuser:
        imagePullSecret:
          enabled: true
          registry: eu.gcr.io
          username: ...
          email: ...
          password: ...
  ```
