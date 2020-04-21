FROM jupyter/datascience-notebook:584e9ab39d22

USER root

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

RUN conda install nb_conda_kernels -y

USER jovyan
