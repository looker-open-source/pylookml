import lookml as l

x = l.lookml.View('order_items')
x + 'id' + 'value'
x.addSum(x.id)
print(x)