.. lookml documentation master file, created by
   sphinx-quickstart on Fri Feb 28 06:12:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyLookML 
=========================================
pyLookML is a metaprogramming interface for the LookML language. It leverages the `lkml <https://pypi.org/project/lkml/>`_ parser to interpret raw lookml files then adds an object oriented API allowing
easy programitic manipulaiton of the file.


Quickstart Examples
-------------------
Install pylookml package via pip

.. code-block:: bash

   pip install lookml

`Make a github access token <https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line>`_

Fetch a viewFile from github and print one of its dimensions

.. code-block:: python
   :linenos:

   import lookml
   proj = lookml.Project(
         repo= "llooker/russ_sandbox",
         access_token="your_github_access_token",
   )
   viewFile = proj.getFile('01_order_items.view.lkml')
   orderItems = viewFile.views.order_items
   print(orderItems.id)

.. code-block:: json

  dimension: id {
    primary_key: yes
    type: number
    sql: ${TABLE}.id ;;
  }


.. toctree::
   :maxdepth: 2
   :caption: Contents:
