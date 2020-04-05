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
   


* Find fields by regex searching a parameter

.. code-block:: python
   :linenos:

   >>> for field in myView.search('sql','\$\{TABLE\}.id'):
   ...     print(field)
   >>>
   dimension: id {
     type: number
     sql: ${TABLE}.id ;;
   }
   dimension: id_order {
     type: string
     sql: ${TABLE}.id_order ;;
   }
   >>> for field in o.search('label','bar'):
   ...     print(field)
   >>>
   dimension: bar {
     type: string
     label: "Bar"
     sql: ${TABLE}.bar ;;
   }
   dimension: bar2 {
     type: string
     label: "Foobar"
     sql: ${TABLE}.bar2 ;;
   }


Fields
------------------------------
.. code-block:: python
   :linenos:

   >>> myView = View('order_items') + 'id'
   >>> print(field.__ref__)
   ${order_items.id}
   >>> print(field.__refs__)
   ${id}
   >>> print(field.__refr__)
   order_items.id
   >>> print(field.__refrs__)
   id

Convenience Methods
------------------------------
* Add a sum measure for every number dimension

.. code-block:: python
   :linenos:

   orderItems.sumAllNumDimensions()


* Change the name of a field and all its child references

.. code-block:: python
   :linenos:

   >>> print(order_items2.shipping_time)

   dimension: shipping_time {
     type: number
     sql: datediff('day',${shipped_raw},${delivered_raw})*1.0 ;;
   }

   >>> for field in order_items2.shipping_time.children():
   ...    print(field)

   measure: average_shipping_time {
     type: average
     value_format_name: decimal_2
     sql: ${shipping_time} ;;
   }

   >>> order_items2.shipping_time.change_name_and_child_references('time_in_transit')
   >>> print(time_in_transit)
   dimension: time_in_transit {
     type: number
     sql: datediff('day',${shipped_raw},${delivered_raw})*1.0 ;;
   }
   >>> for field in order_items2.time_in_transit.children():
   ...    print(field)
   measure: average_shipping_time {
     type: average
     value_format_name: decimal_2
     sql: ${time_in_transit} ;;
   }


