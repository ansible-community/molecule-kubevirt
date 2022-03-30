************************
Molecule KubeVirt Plugin
************************

.. image:: https://badge.fury.io/py/molecule-kubevirt.svg
   :target: https://badge.fury.io/py/molecule-kubevirt
   :alt: PyPI Package

.. image:: https://github.com/jseguillon/molecule-kubevirt/workflows/tox/badge.svg
   :target: https://github.com/jseguillon/molecule-kubevirt/actions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
   :alt: Python Black Code Style

.. image:: https://img.shields.io/badge/license-MIT-brightgreen.svg
   :target: LICENSE
   :alt: Repository License

Molecule KubeVirt Plugin is designed to allow use of KubeVirt_ containers for provisioning test resources.

**Very alpha version - All configuration fields and behaviours may be subject to breaking changes**

.. _`KubeVirt`: https://kubevirt.io

Scope
=====

Molecule-kubevirt enables running ansible roles tests in a kubernetes cluster.

Usage
=====

To use this plugin, you'll need to set the ``driver`` and ``platform``
variables in your ``molecule.yml``. Here's a simple example using a home made centos docker image for KubeVirt:

.. code-block:: yaml

  driver:
    name: kubevirt
  platforms:
    - name: instance
      image: quay.io/kubevirt/fedora-cloud-container-disk-demo

Installation
============

Ansible
-------

This driver supports Ansible 2, 3 and 4.

Ansible 2 requires python requirements pinning to:

.. code-block:: shell

  python3 -m pip install 'openshift==0.11.*' 'kubernetes==11.*'

**No depedency required for Ansible >= 3**


KubeVirt
--------

Get access to a Kubernetes cluster then install KubeVirt for `kind <https://kubevirt.io/quickstart_kind/>`_ or `minkube <https://kubevirt.io/quickstart_minikube/>`_ or `cloud providers <https://kubevirt.io/quickstart_cloud/>`_


SSH access
==========

A Kubernetes Service is created by the driver for SSH access. Current supported Services are ClusterIP and NodePort.

ClusterIP
---------

Default SSH Service is ClusterIP and a static clusterIP can be set:

.. code-block:: yaml

  ssh_service:
    type: ClusterIP
    clusterIP: 10.96.102.231

Please note molecule needs to be able to route ip to ClusterIPs Services:

* if running Kubernetes with kind:

.. code-block:: shell

  IP=$(docker container inspect kind-control-plane   --format '{{ .NetworkSettings.Networks.kind.IPAddress }}')
  sudo ip route add 10.96.0.0/12 via $IP # Linux
  # sudo route -n add 10.96.0.0/12 $IP # MacOSX

* if running Kubernetes with minikube:

.. code-block:: shell

  sudo ip route add 172.17.0.0/16 via $(minikube ip) # Linux
  # sudo route -n add 172.17.0.0/16 $(minikube ip) # MacOSX

If running tox from inside Kubernetes cluster, nothing to do on this item.


NodePort
--------

NodePort can be set. Static nodePort can be defined, also host target for port can be set:

.. code-block:: yaml

  ssh_service:
    type: NodePort
    # optional static port
    nodePort: 32569
    # host where nodePort can be reached
    nodePort_host: localhost


Virtual machines customization
==============================

Virtual machines can be customized using `domain`, `volumes`, `networks` and `user_data`.

Since the driver already sets some values for molecule to start VMs with no customization, values set in those fields will be merged with default configuration.


Disk example
------------

Here is an example on how to customize disks. Please note:

* user_data is an example for Debian-11; other systems may have different disk name than /dev/vdxxx
* since the driver creates one disk for OS, plus one disk for cloud-config, additional disk is third known disk (and gets *'c'* index)

.. code-block:: yaml

    domain:
      devices:
        disks:
          - name: emptydisk
            disk:
              bus: virtio
    volumes:
      - name: emptydisk
        emptyDisk:
          capacity: 2Gi

    user_data: |-
      mounts:
       - [ /dev/vdc, /var/lib/software, "auto", "defaults,nofail", "0", "0" ]
      fs_setup:
        - label: data_disk
          filesystem: 'ext4'
          device: /dev/vdc
          overwrite: true


Run from inside Kubernetes cluster
==================================

You can run this driver with a container running tox and/or molecule. Take a look at:
 * Dockerfile_ as a base image
 * test-rolebinding_ file for ServiceAccount example
 * github_workflow_ in step named "Launch test" for a Kubernetes Job running tox

.. _`test-rolebinding`: /tools/test-rolebinding.yaml
.. _`Dockerfile`: /tools/Dockerfile
.. _`github_workflow`: .github/workflows/tox.yml

Demo
====

Testing nginx ansible role with KubeVirt, via github actions: `jseguillon/ansible-role-nginx <https://github.com/jseguillon/ansible-role-nginx>`_


Get Involved
============

* Join us in the ``#ansible-molecule`` channel on `Freenode`_.
* Join the discussion in `molecule-users Forum`_.
* Join the community working group by checking the `wiki`_.
* Want to know about releases, subscribe to `ansible-announce list`_.
* For the full list of Ansible email Lists, IRC channels see the
  `communication page`_.

.. _`Freenode`: https://freenode.net
.. _`molecule-users Forum`: https://groups.google.com/forum/#!forum/molecule-users
.. _`wiki`: https://github.com/ansible/community/wiki/Molecule
.. _`ansible-announce list`: https://groups.google.com/group/ansible-announce
.. _`communication page`: https://docs.ansible.com/ansible/latest/community/communication.html

.. _license:

License
=======

The `MIT`_ License.

.. _`MIT`: https://github.com/jseguillon/molecule-kubevirt/blob/master/LICENSE

The logo is licensed under the `Creative Commons NoDerivatives 4.0 License`_.

If you have some other use in mind, contact us.

.. _`Creative Commons NoDerivatives 4.0 License`: https://creativecommons.org/licenses/by-nd/4.0/
