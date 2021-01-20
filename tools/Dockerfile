ARG PYTHON_BASE_IMAGE

FROM ${PYTHON_BASE_IMAGE}
ARG KUBERNETES_VERSION

RUN python3 -m pip install tox ansible openshift jmespath && \
      ansible-galaxy collection install community.crypto && \
      ansible-galaxy collection install git+https://github.com/ansible-collections/community.kubernetes.git

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/${KUBERNETES_VERSION}/bin/linux/amd64/kubectl && \
      chmod +x kubectl && mv kubectl /usr/bin

COPY . /opt/molecule_kubevirt
