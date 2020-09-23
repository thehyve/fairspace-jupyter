FROM jupyter/datascience-notebook:lab-2.0.1

USER root

RUN apt-get update && \
    apt-get install -y vim curl fusedav && \
    rm -rf /var/lib/apt/lists/*

ADD start /
RUN chown jovyan:users /start
RUN chmod u+x /start

ADD app.js /opt/proxy/
ADD package.json /opt/proxy/
WORKDIR /opt/proxy
RUN npm install

ADD atomiclargefilemanager.py /opt/conda/lib/python3.7/site-packages/notebook/services/contents/
RUN echo "" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "from notebook.services.contents.atomiclargefilemanager import AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.contents_manager_class = AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.FileCheckpoints.checkpoint_dir = '/home/jovyan/.notebookCheckpoints'" >> /etc/jupyter/jupyter_notebook_config.py

RUN pip install sparqlkernel
RUN jupyter sparqlkernel install

RUN conda install nb_conda_kernels -y

USER jovyan
WORKDIR /home/jovyan