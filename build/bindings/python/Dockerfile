#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

ARG base_img

FROM $base_img
WORKDIR /

ARG python_version='3.8.8'
ENV PYTHON_BUILD_VERSION=$python_version

# Reset to root to run installation tasks
USER 0

RUN mkdir ${SPARK_HOME}/python

# Custom python version install ( https://linuxize.com/post/how-to-install-python-3-8-on-debian-10/ )
RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev && \
    curl -O https://www.python.org/ftp/python/${PYTHON_BUILD_VERSION}/Python-${PYTHON_BUILD_VERSION}.tar.xz && \
    tar -xf Python-${PYTHON_BUILD_VERSION}.tar.xz && \
    cd Python-${PYTHON_BUILD_VERSION} && \
    ./configure --enable-optimizations && \
    make -j 4 && \
    make altinstall && \
    cd .. && rm -rf Python-${PYTHON_BUILD_VERSION}* && \
    ln -sf /usr/local/bin/python3.8 /usr/bin/python3 && \
    ln -sf /usr/local/bin/pip3.8 /usr/bin/pip3 && \
    pip3 install --upgrade pip setuptools && \
    apt remove -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev && \
    rm -rf /var/cache/apt/*

#RUN apt-get update && \
#    apt install -y python3 python3-pip && \
#    pip3 install --upgrade pip setuptools && \
#    # Removed the .cache to save space
#    rm -r /root/.cache && rm -rf /var/cache/apt/*

RUN ln -s /usr/bin/python3 /usr/bin/python2

COPY python/pyspark ${SPARK_HOME}/python/pyspark
COPY python/lib ${SPARK_HOME}/python/lib

WORKDIR /opt/spark/work-dir
ENTRYPOINT [ "/opt/entrypoint.sh" ]

# Specify the User that the actual main process will run as
ARG spark_uid=185
USER ${spark_uid}
