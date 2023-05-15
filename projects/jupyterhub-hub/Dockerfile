FROM jupyterhub/k8s-hub:2.0.0

ADD fairspace.py /usr/local/lib/python3.9/site-packages/oauthenticator/

USER root

RUN chmod 0644 /usr/local/lib/python3.9/site-packages/oauthenticator/fairspace.py

USER jovyan
