#!/usr/bin/env bash

here=$(realpath $(dirname "${0}"))
helm_cmd=$(realpath ~/bin/helm3/helm)

# Prerequisites:
# $ minikube start
# $ minikube addons enable ingress

host_address=$(minikube ssh grep host.minikube.internal /etc/hosts | cut -f1)

pushd "${here}"
eval $(minikube docker-env) && \
(docker build ../../projects/jupyterhub-hub -t jupyterhub-hub-local:latest && docker build ../../projects/jupyterhub-singleuser -t jupyterhub-singleuser-local:latest) || {
  echo "Build failed."
  popd
  exit 1
}

(kubectl get ns jupyterhub-dev || kubectl create ns jupyterhub-dev) && \
((${helm_cmd} repo list | cut -f1 | grep '^jupyterhub') || ${helm_cmd} repo add jupyterhub https://jupyterhub.github.io/helm-chart) && \
${helm_cmd} dependency update ../../charts/jupyter && \
${helm_cmd} package ../../charts/jupyter && \
${helm_cmd} upgrade jupyterhub-local --install --namespace jupyterhub-dev jupyter-0.0.0-RELEASEVERSION.tgz \
  -f local-values.yaml

popd
