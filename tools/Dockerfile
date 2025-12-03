ARG PYTHON_BASE_IMAGE=python:3.11

FROM ${PYTHON_BASE_IMAGE}
ARG KUBERNETES_VERSION

RUN python3 -m pip install tox

RUN curl -LO curl -LO https://dl.k8s.io/release/${KUBERNETES_VERSION}/bin/linux/amd64/kubectl && \
      chmod +x kubectl && mv kubectl /usr/bin


# FIXME : DO NOT COPY . => MANY UNWANTED FILES !!!
COPY . /opt/molecule_kubevirt
