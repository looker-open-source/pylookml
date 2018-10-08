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

```
#More advanced example:
import lookml

order_items = lookml.View('order_items').setSqlTableName(sql_table_name='public.order_items')
order_items + 'id' + 'value' + 'inventory_item_id'
order_items.id.setNumber()
order_items.inventory_item_id.setNumber()
order_items.addSum('value')
order_items + lookml.DimensionGroup('created_at') 

products = lookml.View('products')
products + 'id' + 'name'

inventory_items = lookml.View('inventory_items').setSqlTableName(sql_table_name='public.inventory_items')
inventory_items + 'id' + 'product_id'


order_items_explore = lookml.Explore(order_items)
order_items_explore.addJoin(inventory_items).on(order_items.inventory_item_id , ' = ', inventory_items.id).setType('left_outer').setRelationship('one_to_one')
order_items_explore.addJoin(products).on(inventory_items.product_id , ' = ', products.id).setType('left_outer').setRelationship('many_to_one')



the_look = lookml.Model('the_look')
the_look.setConnection('my_connection')
the_look.include(order_items)
the_look.include(inventory_items)
the_look.addExplore(order_items_explore)


the_look.order_items.order_items.id.addLink(
    url='/dashboards/7?brand=cool',
    label=''
)

product_facts_ndt = order_items_explore.createNDT(explore_source=order_items_explore, name='product_facts_ndt',fields=[products.id,order_items.total_value])
product_facts_ndt.addSum('total_value')
the_look.include(product_facts_ndt)
product_facts_ndt.write()
order_items_explore.addJoin(product_facts_ndt).on(products.id,' = ',product_facts_ndt.id).setType('left_outer').setRelationship('one_to_one')

the_look.write()
order_items.write()
products.write()
inventory_items.write()


```



