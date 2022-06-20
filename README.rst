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

.. _`KubeVirt`: https://kubevirt.io

Supported Platforms
===================

Works with any OS distributed as cloud-config_ compatible image (also known as "Cloud images").

.. _`cloud-config`: https://cloudinit.readthedocs.io/en/latest/topics/availability.html

Usage
=====

To use this plugin, you'll need to set the ``driver`` and ``platform`` variables in your ``molecule.yml``:

.. code-block:: yaml

  driver:
    name: kubevirt
  platforms:
    - name: instance
      image: quay.io/kubevirt/fedora-cloud-container-disk-demo

Installation
============

Driver
------

This driver supports Ansible 2, 3 and 4.

.. code-block:: shell

  # Ansible >2
  python3 -m pip install molecule-kubevirt

  # Ansible 2
  python3 -m pip install molecule-kubevirt 'openshift<0.12.0' 'kubernetes<12.0'


KubeVirt Installation
---------------------

Follow KubeVirt guides for `kind <https://kubevirt.io/quickstart_kind/>`_, `minkube <https://kubevirt.io/quickstart_minikube/>`_, or `cloud providers <https://kubevirt.io/quickstart_cloud/>`_


SSH access
==========

By default, the driver connects onto ssh via VirtualMachineInstance Pod ip and molecule needs to be able to ssh directly to Pod ip:

* if running local Kubernetes with kind:

.. code-block:: shell

  IP=$(docker container inspect kind-control-plane --format '{{ .NetworkSettings.Networks.kind.IPAddress }}')
  sudo ip route add 10.244.0.0/16 via $IP # Linux
  # sudo route -n add 10.244.0.0/16 $IP # MacOSX

* if running local Kubernetes with minikube:

.. code-block:: shell

  sudo ip route add 172.17.0.0/16 via $(minikube ip)
  # sudo route -n add 172.17.0.0/16 $(minikube ip) # MacOSX

* if running molecule inside the target Kubernetes cluster, routing is ensured by CNI.

A Kubernetes Service can be created by the driver for SSH access. Current supported Services are ClusterIP and NodePort.

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

ClusterIP
---------

Default SSH Service is ClusterIP and a static clusterIP can be set:

.. code-block:: yaml

  ssh_service:
    type: ClusterIP
    clusterIP: 10.96.102.231

Molecule then needs to be able to ssh on the ClusterIP ip:

* if running local Kubernetes with Kind:

.. code-block:: shell

  IP=$(docker container inspect kind-control-plane   --format '{{ .NetworkSettings.Networks.kind.IPAddress }}')
  sudo ip route add 10.96.0.0/12 via $IP # Linux
  # sudo route -n add 10.96.0.0/12 $IP # MacOSX

* if running local Kubernetes with Minikube, no known solution yet.
* if running molecule inside the target Kubernetes cluster, routing is ensured by CNI.


Virtual machines customisation
==============================

A few defaults are created if not provided in platfom definition:

* if no interface with :code:`name: default` is defined in :code:`domain.devices.interfaces`, then a default one is created with :code:`brige: {}` and :code:`bus: virtio`,
* if no disk with :code:`name: boot` is defined in :code:`domain.devices.disks`, then a default one is created with :code:`bus: virtio`,
* if no network with :code:`name: default` is defined in :code:`networks`, then a default one is created with :code:`pod: {}` and :code:`model: virtio`,
* if no volume with :code:`name: boot` is defined in :code:`volumes`, then a default one is created as:

  * a :code:`containerDisk`
  * with :code:`image`, :code:`path` and :code:`imagePullPolicy` respectively set to plaform :code:`image`, :code:`image_path` and :code:`image_pull_policy`

* if cloud-config is defined in :code:`user_data` it is merged default one wich sets ssh public key for 'molecule' user.

Customisation example
---------------------

This example configuration demonstrates how to:

* use Kubevirt's CDI in place of an :code:`image` using :code:`dataVolumeTemplates` and overriding default :code:`boot` volume.
* set customs ressources and annotation
* and a second interface/network
* adds a second disk/volume
* make use of cloud-config to format and mount additional disk

.. code-block:: yaml

  ---
  dependency:
    name: galaxy
  driver:
    name: kubevirt
  platforms:
    - name: instance
      # annotate for calico static ip
      annotations:
        cni.projectcalico.org/ipAddrs: "[\"10.244.25.25\"]"
      # use data volume facility in place of using 'image:'
      dataVolumeTemplates:
        - metadata:
            name: disk-dv
          spec:
            pvc:
              accessModes:
              - ReadWriteOnce
              resources:
                requests:
                  storage: 10Gi
            preallocation: true
            source:
              http:
                url: https://download.fedoraproject.org/pub/fedora/linux/releases/35/Cloud/x86_64/images/Fedora-Cloud-Base-35-1.2.x86_64.raw.xz
      domain:
        resources:
          limits:
            cpu: "1"
            memory: 3Gi
          requests:
            cpu: 200m
            memory: 1Gi
        devices:
          interfaces:
            # add a second device interface
            - bridge: {}
              name: multus
              model: virtio
              ports:
                - port: 22
          disks:
            # add a second device disk
            - name: emptydisk
              disk:
                bus: virtio
      volumes:
          # override default 'boot' volume with cdi data volume template source
        - name: boot
          dataVolume:
            name: disk-dv
        # add a second volume, must be same name as defined in device
        - name: emptydisk
          emptyDisk:
            capacity: 2Gi
      networks:
        # add a second network for added device interface
        - name: multus
          multus:
            # use a NetworkAttachement
            networkName: macvlan-conf
      # cloud-config format and mount additional disk
      user_data:
        # format additional disk
        fs_setup:
          - label: data_disk
            filesystem: 'ext4'
            device: /dev/vdb
            overwrite: true
        # mount additional disk
        mounts:
          - [ /dev/vdb, /var/lib/software, "auto", "defaults,nofail", "0", "0" ]

See `molecule/tests/molecule.yml` from source code for full example.

Run from inside Kubernetes cluster
==================================

You can run this driver with a container running tox and/or molecule. Take a look at:

* Dockerfile_ as a base image
* test-rolebinding_ file for ServiceAccount example
* github_workflow_ in step named "Launch test" for a Kubernetes Job running tox

.. _`test-rolebinding`: /tools/test-rolebinding.yaml
.. _`Dockerfile`: /tools/Dockerfile
.. _`github_workflow`: .github/workflows/tox.yml


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
