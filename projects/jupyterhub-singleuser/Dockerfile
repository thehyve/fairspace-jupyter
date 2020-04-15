FROM jupyter/datascience-notebook:dc9744740e12

USER root

RUN echo 'deb http://archive.ubuntu.com/ubuntu/ bionic-proposed restricted main multiverse universe' >> /etc/apt/sources.list.d/proposed-repositories.list
RUN apt-get update && \
    apt-get install -y vim curl nginx davfs2 && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 80

RUN echo "$NB_USER ALL=(ALL) NOPASSWD: /usr/sbin/nginx" >> /etc/sudoers

ADD start /
RUN chmod a+rx /start

ADD atomiclargefilemanager.py /opt/conda/lib/python3.7/site-packages/notebook/services/contents/
RUN echo "" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "from notebook.services.contents.atomiclargefilemanager import AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.contents_manager_class = AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.FileCheckpoints.checkpoint_dir = '/home/jovyan/.notebookCheckpoints'" >> /etc/jupyter/jupyter_notebook_config.py

RUN chmod u+s /sbin/mount.davfs
RUN echo 'http://localhost/webdav/ /home/jovyan/collections davfs user,noauto,file_mode=600,dir_mode=700 0 1' >> /etc/fstab
RUN usermod -a -G davfs2 jovyan

