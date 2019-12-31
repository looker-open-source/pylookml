connection: "my_connection"
include: "order_items.view.lkml"
include: "inventory_items.view.lkml"
include: "product_facts_ndt.view.lkml"





explore: order_items {
    
join: inventory_items {
    sql_on: ${order_items.inventory_item_id} = ${inventory_items.id} ;;
    type: left_outer
    relationship: one_to_one
}

    
join: products {
    sql_on: ${inventory_items.product_id} = ${products.id} ;;
    type: left_outer
    relationship: many_to_one
}

    
join: product_facts_ndt {
    sql_on: ${products.id} = ${product_facts_ndt.id} ;;
    type: left_outer
    relationship: one_to_one
}

}
