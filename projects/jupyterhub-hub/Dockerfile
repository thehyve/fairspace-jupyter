FROM jupyterhub/k8s-hub:0.9.0

ADD fairspace.py /usr/local/lib/python3.6/dist-packages/oauthenticator/

USER root

RUN chmod 0644 /usr/local/lib/python3.6/dist-packages/oauthenticator/fairspace.py

USER jovyan