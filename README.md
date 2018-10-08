This is a pythonic api for creating LookML objects.

get started fast:
`pip install lookml`

```
import lookml

#create a new view
order_items = lookml.View('order_items')

# add a couple fields
order_items + 'id' + 'value'

# add a sum measure
order_itmems.addSum('id')

# order_items.view.lkml will be written in working directory
order_items.write()

```

Readme TODO:

create a model

create an explore

create a view with a dimension and a few measures

create a join between two views

create a star schema

create a calendar table

create an NDT(not possible within the API yet)



