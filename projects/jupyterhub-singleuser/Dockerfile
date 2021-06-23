FROM jupyter/datascience-notebook:lab-3.0.16

USER root

RUN apt-get update && \
    apt-get install -y vim curl fusedav && \
    rm -rf /var/lib/apt/lists/* /var/log/dpkg.log /var/log/apt/*

ADD start /
RUN chown jovyan:users /start
RUN chmod u+x /start

ADD app.js /opt/proxy/
ADD package.json /opt/proxy/
WORKDIR /opt/proxy
RUN npm install

ADD atomiclargefilemanager.py /opt/conda/lib/python3.9/site-packages/notebook/services/contents/
RUN echo "" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "from notebook.services.contents.atomiclargefilemanager import AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.contents_manager_class = AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.FileCheckpoints.checkpoint_dir = '/home/jovyan/.notebookCheckpoints'" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.FileManagerMixin.use_atomic_writing = False" >> /etc/jupyter/jupyter_notebook_config.py

RUN pip install sparqlkernel && \
    jupyter sparqlkernel install

ENV JUPYTER_COMMAND=${JUPYTER_COMMAND:-jupyterhub-singleuser}

RUN chown jovyan:users /home/jovyan/.local/share/jupyter
USER jovyan
WORKDIR /home/jovyan
