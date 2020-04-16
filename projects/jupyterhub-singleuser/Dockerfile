FROM jupyter/scipy-notebook:d4cbf2f80a2a

USER root

# RUN echo 'deb http://archive.ubuntu.com/ubuntu/ bionic-proposed restricted main multiverse universe' >> /etc/apt/sources.list.d/proposed-repositories.list
RUN apt-get update && \
    apt-get install -y vim curl nginx fusedav && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 80

RUN echo "$NB_USER ALL=(ALL) NOPASSWD: /usr/sbin/nginx" >> /etc/sudoers

ADD start /
RUN chown jovyan:users /start
RUN chmod u+x /start

ADD atomiclargefilemanager.py /opt/conda/lib/python3.7/site-packages/notebook/services/contents/
RUN echo "" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "from notebook.services.contents.atomiclargefilemanager import AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.contents_manager_class = AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.FileCheckpoints.checkpoint_dir = '/home/jovyan/.notebookCheckpoints'" >> /etc/jupyter/jupyter_notebook_config.py

USER jovyan
