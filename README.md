pyLookML allows you to fetch, parse and program lookml very easily. 
It is an object oriented metaprogramming interface built on top of the AWESOME lkml parsing library which you can check out here: https://github.com/joshtemple/lkml. But extends it by adding convenience to it's json structure and more advanced integrations and object oriented behaviors.
Check out the full documentation for pyLookml project here: https://pylookml.readthedocs.io/en/latest/

In the meantime here are some very basic examples for getting started:

get started fast:
`pip install lookml`

Connect to a lookml github project:
```
   import lookml
   proj = lookml.Project(
         repo= "llooker/russ_sandbox",
         access_token="your_github_access_token",
   )
   viewFile = proj.getFile('01_order_items.view.lkml')
   orderItems = viewFile.views.order_items
   print(orderItems.id)
```

Pure lookml generation:
```
import lookml

#create a new view
order_items = lookml.View('order_items')

# add a couple fields
order_items + 'id' + 'value'

# add a sum measure
order_items.addSum('id')

# order_items.view.lkml will be written in working directory
order_items.write()

```
