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
      image: quay.io/jseguillon/kubevirt-images:centos-7-x86_64-genericcloud-2009

This driver also requires molecule to access Kubernetes API. See test-rolebinding_ file.

.. _`test-rolebinding`: /tools/test-rolebinding.yaml


Installation
============

Ansible
-------

This driver supports Ansible 2, 3 and 4.

Ansible 2 requires install of comunity.kubevirt plus strict python requirements pinning:

.. code-block:: shell

  ansible-galaxy install git+https://github.com/ansible-collections/community.general.git
  python3 -m pip install openshift==0.11.2 kubernetes==11.0.0

**No depedency required for Ansible >= 3**


KubeVirt
--------

Get access to a Kubernetes cluster then install KubeVirt for `kind <https://kubevirt.io/quickstart_kind/>`_ or `minkube <https://kubevirt.io/quickstart_minikube/>`_ or `cloud providers <https://kubevirt.io/quickstart_cloud/>`_


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
