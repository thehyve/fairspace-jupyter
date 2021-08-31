FROM jupyter/datascience-notebook:lab-3.0.16

USER root

RUN apt-get update && \
    apt-get install -y vim curl sudo libneon27-gnutls-dev po4a automake && \
    rm -rf /var/lib/apt/lists/* /var/log/dpkg.log /var/log/apt/*

RUN curl -fL https://github.com/thehyve/davfs2/archive/refs/heads/fairspace.zip -o davfs2-fairspace.zip && \
    unzip davfs2-fairspace.zip && \
    cd davfs2-fairspace && \
    ./bootstrap && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -r davfs2-*

RUN addgroup --system davfs2 && \
    adduser --system davfs2 && \
    adduser davfs2 davfs2 && \
    adduser jovyan davfs2

ADD start /
RUN chown jovyan:users /start
RUN chmod u+x /start

ADD dav_mount /usr/local/bin/
RUN chmod u+x /usr/local/bin/dav_mount
RUN echo "%davfs2 ALL=(ALL) NOPASSWD: /usr/local/bin/dav_mount *" > /etc/sudoers.d/dav_mount
RUN echo "ask_auth 0" >> /usr/local/etc/davfs2/davfs2.conf; \
    echo "use_proxy 0" >> /usr/local/etc/davfs2/davfs2.conf; \
    echo "use_locks 0" >> /usr/local/etc/davfs2/davfs2.conf; \
    echo "min_propset 1" >> /usr/local/etc/davfs2/davfs2.conf; \
    echo "gui_optimize 1" >> /usr/local/etc/davfs2/davfs2.conf; \
    echo "file_refresh 60" >> /usr/local/etc/davfs2/davfs2.conf; \
    echo "dir_refresh 60" >> /usr/local/etc/davfs2/davfs2.conf

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
