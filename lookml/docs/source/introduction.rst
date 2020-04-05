
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

.. code-block:: 

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


