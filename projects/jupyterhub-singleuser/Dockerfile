FROM jupyter/datascience-notebook:r-3.6.3

USER root

RUN apt-get update && \
    apt-get install -y vim curl fuse libneon27-gnutls && \
    rm -rf /var/lib/apt/lists/*

ADD start /
RUN chown jovyan:users /start
RUN chmod u+x /start

RUN curl -sLO http://security.ubuntu.com/ubuntu/pool/universe/f/fusedav/fusedav_0.2-3.1build1_amd64.deb && dpkg -i fusedav_0.2-3.1build1_amd64.deb
RUN rm fusedav_0.2-3.1build1_amd64.deb

ADD app.js /opt/proxy/
ADD package.json /opt/proxy/
WORKDIR /opt/proxy
RUN npm install

ADD atomiclargefilemanager.py /opt/conda/lib/python3.7/site-packages/notebook/services/contents/
RUN echo "" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "from notebook.services.contents.atomiclargefilemanager import AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.contents_manager_class = AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.FileCheckpoints.checkpoint_dir = '/home/jovyan/.notebookCheckpoints'" >> /etc/jupyter/jupyter_notebook_config.py

RUN conda install nb_conda_kernels -y

USER jovyan
WORKDIR /home/jovyan