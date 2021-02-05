Change Log
----------
Starting with PyLookML version 3.0.0

3.0.3

* fixed an issue with the constructor not accepting lookML names with numbers `Issue Link <https://github.com/llooker/pylookml/issues/43>`_.

The following code now works:

.. code-block:: python

  my_dim = lookml.Dimension('dimension: custom_5 {}')

3.0.0

* complete and more stable re-write geared toward maximum backward compatibility 

* language complete for all the latest LookML language updates (as of Looker 7.20) (new filters, materializations etc)

* significantly better whitespace handling

* can connect to filesystem without git

* added a CLI with various functions, including project dir list and autotune

* added new operator overloading syntax

* more helpful error messages

* options such as OMIT_DEFAULTS = true


