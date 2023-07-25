FROM jupyter/datascience-notebook:lab-3.6.3

USER root

RUN apt-get update && \
    apt-get install -y vim curl sudo libneon27-gnutls-dev po4a automake && \
    rm -rf /var/lib/apt/lists/* /var/log/dpkg.log /var/log/apt/*

USER ${NB_UID}

RUN mamba install --yes -c 'bioconda' \
    'bioconductor-genomeinfodbdata=1.2.9' \
    'bioconductor-phyloseq' \
    'bioconductor-deseq2' \
    'bioconductor-clusterprofiler' \
    'bioconductor-microbiome' \
    'rtk'

RUN mamba install --yes -c 'conda-forge' \
    'r-dplyr' \
    'r-ggrepel' \
    'r-cowplot' \
    'r-coin' \
    'r-rtsne' \
    'r-svmisc' \
    'r-vegan' \
    'r-venndiagram' \
    'r-rjava' \
    'r-fuzzyjoin' \
    'r-plotly' \
    'pyqt' \
    'scikit-learn' \
    'shap' \
    'scipy' \
    'catboost' \
    'orange3'

RUN mamba clean --all -f -y

RUN R -e "devtools::install_github('beadyallen/MGnifyR')"
RUN R -e "devtools::install_github('aberHRML/metabolighteR')"
RUN R -e 'install.packages("rtk", repos = "https://cloud.r-project.org")'

RUN fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

USER root

RUN curl -fL https://github.com/thehyve/davfs2/archive/refs/heads/fairspace_davfs2_upgrade.zip -o davfs2-fairspace_davfs2_upgrade.zip && \
    unzip davfs2-fairspace_davfs2_upgrade.zip && \
    cd davfs2-fairspace_davfs2_upgrade && \
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
RUN chown jovyan:users /start && \
    chmod u+x /start && \
    chmod u+x /etc/fstab

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

ADD atomiclargefilemanager.py /opt/conda/lib/python3.10/site-packages/notebook/services/contents/
RUN echo "" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "from notebook.services.contents.atomiclargefilemanager import AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.contents_manager_class = AtomicLargeFileManager" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.FileCheckpoints.checkpoint_dir = '/home/jovyan/.notebookCheckpoints'" >> /etc/jupyter/jupyter_notebook_config.py && \
    echo "c.FileManagerMixin.use_atomic_writing = False" >> /etc/jupyter/jupyter_notebook_config.py

ENV JUPYTER_COMMAND=${JUPYTER_COMMAND:-jupyterhub-singleuser}

RUN sudo chown -R jovyan:users /home/jovyan/.jupyter/

USER jovyan
WORKDIR /home/jovyan
