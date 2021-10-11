ARG PYTHON_BASE_IMAGE

FROM ${PYTHON_BASE_IMAGE}
ARG KUBERNETES_VERSION

RUN python3 -m pip install tox

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/${KUBERNETES_VERSION}/bin/linux/amd64/kubectl && \
      chmod +x kubectl && mv kubectl /usr/bin


# FIXME : DO NOT COPY . => MANY UNWANTED FILES !!!
COPY . /opt/molecule_kubevirt
