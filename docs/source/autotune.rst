Autotune your model using PyLookML
------------------------------

PyLookML offers a command line interface (CLI) which offers several commands, one of which is autotune.
It will automatically create aggregate awareness tables inside of your LookML model based on the most frequently run queries and commit to a
developer branch so that you can confirm the output first.

Let's get started with an example:
ensure that you have installed it using pip, which will bind the lookml command. **Note**: if you install it in a virtual environment 
the lookml command will only be available when the virtual environment is active.

pip install lookml 

lookml autotune useconfig
*will automatically look for autotune.ini in your current directory, if not found it will ask for a path

lookml autotune
*will ask for each piece of information required as a step by step



