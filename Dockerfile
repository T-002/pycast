FROM python:3.7

ENV PACKAGE_NAME="pycast"
ENV BASE_DIR=/$PACKAGE_NAME

ENV PACKAGE_DIR=$BASE_DIR/$PACKAGE_NAME
ENV TEST_DIR=$BASE_DIR/tests
ENV DOC_DIR=$BASE_DIR/doc
ENV BUILD_DIR=$BASE_DIR/_build

RUN  apt-get update && \
     apt-get install make -y
RUN  apt-get clean -y

RUN  mkdir -p $BASE_DIR
RUN  mkdir -p $BUILD_DIR

# Download and install dependencies
COPY requirements.txt /$BASE_DIR
RUN  pip install --upgrade pip && \
     pip install \
         --upgrade \
         -r $BASE_DIR/requirements.txt

# Copy all content into the container
COPY $PACKAGE_NAME $PACKAGE_DIR
COPY tests $TEST_DIR
COPY doc $DOC_DIR
COPY conf.py $BASE_DIR
COPY Makefile /$BASE_DIR
COPY readme.rst /$BASE_DIR
COPY setup.py $BASE_DIR

RUN echo 'eval $(thefuck --alias)' >> /etc/bash.bashrc

ENV PYTHONPATH=$BASE_DIR
WORKDIR $BASE_DIR
