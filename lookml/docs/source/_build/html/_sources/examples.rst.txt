Cookbook / Examples
================================

Basic Recipes 
-------------------


* connect to your github project

.. code-block:: python
   :linenos:

   import lookml
   proj = lookml.Project(
         repo= "llooker/russ_sandbox",
         access_token="your_github_access_token",
   )

Or do the same thing from any other git service (as long as you have SSH git access on the machine pyLookML is running on):

.. code-block:: python
   :linenos:

        proj = lookml.Project(
                 git_url='git@bitbucket.org:myorg/russ_sandbox.git'
                 #Optional args for the deploy URL (for deploying directly to prodcution mode)
                ,looker_host="https://mylooker.looker.com/"
                ,looker_project_name="my_project"
        )

* Loop over the views in a file

.. code-block:: python
   :linenos:

   myFile = proj.file('01_order_items.view.lkml')
   #Loops over 1:n views in the file
   for view in myFile.views:
       print(view)


* Write your files back to github

.. code-block:: python
   :linenos:

   viewFile = proj.file('01_order_items.view.lkml')
   viewFile.views.order_items.id.addTag("hello, World!")
   proj.updateFile(viewFile)

* Loop over fields of a certain type

.. code-block:: python
   :linenos:

   >>> for dim in myFile.views.order_items.dims():
   ...     print(dim.__ref__)
   ... 
   ${order_items.new_dimension}
   ${order_items.id}
   ${order_items.cpt_code_value}
   ${order_items.inventory_item_id}
   ... 
   >>> for meas in myFile.views.order_items.measures():
   ...     print(meas.__ref__)
   ... 
   ${order_items.count}
   ${order_items.min_sale_price}
   ${order_items.max_sale_price}
   ${order_items.order_count}
   >>> for flt in myFile.views.order_items.filters():
   ...     print(flt.__ref__)
   ... 
   ${order_items.cpt_code}
   ${order_items.cohort_by}
   ${order_items.metric}

* check all of the children / descendants of a field

.. code-block:: python
   :linenos:

   >>> for child in order_items.sale_price.children():
   ...     print(child.__refs__)
   ... 
   ${min_sale_price}
   ${max_sale_price}
   ${total_sale_price}
   ${average_sale_price}
   ${median_sale_price}
   ${returned_total_sale_price}
   ${gross_margin}
   ${item_gross_margin_percentage}


* search a view for dimensions who's properties match a regex pattern (Find view fields by regex searching any parameter)

.. code-block:: python
   :linenos:

   >>> for item in order_items.search('sql','\$\{shipped_raw\}'):
   ...     print(item.__ref__)
   ...     print(item.sql)
   ... 
   ${order_items.shipping_time}
   sql: datediff('day',${shipped_raw},${delivered_raw})*1.0 ;;


* Add a new view to an existing file

.. code-block:: python
   :linenos:

   myNewView = lookml.View('hello_world')
   myFile = proj.file('01_order_items.view.lkml')
   myFile + myNewView
   for view in myFile.views:
      print(view.name)
   >>> 'order_items'
   >>> 'hello_world'


* Get fields by tag, do work, remove tag

.. code-block:: python
   :linenos:

   for field in orderItems.getFieldsByTag('x'):
      #do work
      field.removeTag('x')

* Add a comment to the tag

.. code-block:: python
   :linenos:

   #results in a comment above the dimension
   orderItems.id.setMessage("Hello I'm Automated")
   

* Create an extended view

.. code-block:: python
   :linenos:

   viewFile = proj.getFile('01_order_items.view.lkml')
   order_items = viewFile.views.order_items
   order_items.extend()
   #this will print both order_items and order_items_extended 
   #(pylookml captures the parent child relationship here)
   print(order_items)
   


Field References
-------------------

.. code-block:: python
   :linenos:

   >>> myView = View('order_items') + 'id'
   >>> print(myView.id)
   dimension: id {
      
      }
   #__ref__ stands for reference
   >>> print(myView.id.__ref__)
   ${order_items.id}
   #__refs__ stands for reference short
   >>> print(myView.id.__refs__)
   ${id}
   #__refr__ stands for reference raw
   >>> print(myView.id.__refr__)
   order_items.id
   #__refrs__ stands for reference raw short
   >>> print(myView.id.__refrs__)
   id

Convenience Methods 
-------------------

* Add a sum measure for every number dimension on a view

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
   #The setName_safe method previously change_name_and_child_references, use that if setName_safe not found
   >>> order_items2.shipping_time.setName_safe('time_in_transit')
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


* working with a local file (The setName_safe method previously change_name_and_child_references, use that if setName_safe not found)


.. code-block:: python

   myFile = lookml.File('example.view.lkml')
      for v in myFile.views:
         for f in v.measures():
               if f.type.value == 'sum' and not f.name.endswith('_total'):
                  f.name = f.setName_safe(f.name + '_total')
      #Optionally Change the location
      myFile.setFolder('pathto/other/folder')
      #Write the file
      x.write()



