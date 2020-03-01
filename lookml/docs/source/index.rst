.. lookml documentation master file, created by
   sphinx-quickstart on Fri Feb 28 06:12:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyLookML 
=========================================
pyLookML is a metaprogramming interface for the LookML language. It leverages the `lkml <https://pypi.org/project/lkml/>`_ parser to interpret raw lookml files then adds an object oriented API allowing
easy programitic manipulaiton of the file. Visit the repo `here <https://github.com/llooker/lookml/>`_:


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


Build from a developer version
------------------------------

*Step 1) Create a virtual env from a clean python and install the dependencies*

.. code-block:: bash

   which python3 #(this is generally the best interpreter use as the startingpoint)
   #Output: /Library/Frameworks/Python.framework/Versions/3.8/bin/python3
   mkdir lookml_test
   cd lookml_test
   virtualenv -p /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 lookml_test_env
   source lookml_test_env/bin/activate
   pip install pygithub
   pip install lkml

*Step 2) go to github and look for the specific commit you'd like to build and replace it in the following command after the @ sign* 

.. code-block:: bash

   pip install git+https://github.com/llooker/lookml.git@04dbd05dd3f37a7fa624501a370df52af26bb5fc


Basic Recipes
------------------------------

* connect to your github project

.. code-block:: python
   :linenos:

   import lookml
   proj = lookml.Project(
         repo= "llooker/russ_sandbox",
         access_token="your_github_access_token",
   )


* Loop over the views in a file

.. code-block:: python
   :linenos:

   viewFile = proj.getFile('01_order_items.view.lkml')
   #Loops over 1:n views in the file
   for view in viewFile.views:
       print(view)


* Write your files back to github

.. code-block:: python
   :linenos:

   viewFile = proj.getFile('01_order_items.view.lkml')
   viewFile.views.order_items.id.addTag("hello, World!")
   proj.updateFile(viewFile)

* Loop over fields of a certain type

.. code-block:: python
   :linenos:

   #TODO


* Add a new view to an existing file

.. code-block:: python
   :linenos:

   #TODO



* Add a sum measure for every number dimension

.. code-block:: python
   :linenos:

   orderItems.sumAllNumDimensions()

* Get fields by tag, do work, remove tag

.. code-block:: python
   :linenos:

   for field in orderItems.getFieldsByTag('x'):
      #do work
      field.removeTag('x')

* Add a comment to the tag

.. code-block:: python
   :linenos:

   orderItems.id.setMessage("Hello I'm Automated")
   #results in a comment above the dimension



* Create an extended view

.. code-block:: python
   :linenos:

   viewFile = proj.getFile('01_order_items.view.lkml')
   order_items = viewFile.views.order_items
   order_items.extend()
   #this will print both order_items and order_items_extended 
   #(pylookml captures the parent child relationship here)
   print(order_items)
   


* Find fields by regex searching their sql

.. code-block:: python
   :linenos:

   >>> for field in o.getFieldBySql('\d{1,3}'):
   ...     print(field)
   >>>
   dimension: foo {
     type: string
     sql: _FINDME_123_ ;;
   }
   





.. toctree::
   :maxdepth: 2
   :caption: Contents:
