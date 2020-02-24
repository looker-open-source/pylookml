
explore: order_items {
    label: "(1) Orders, Items and Users"
    view_name: order_items
join: order_facts {
    type: left_outer
  view_label: "Orders"
  relationship: many_to_one
  sql_on: FOO ;;
}

    
join: inventory_items {
    type: full_outer
  relationship: one_to_one
  sql_on: ${inventory_items.id} = ${order_items.inventory_item_id} ;;
}

    
join: users {
    type: left_outer
  relationship: many_to_one
  sql_on: ${order_items.user_id} = ${users.id} ;;
}

    
join: user_order_facts {
    view_label: "Users"
  type: left_outer
  relationship: many_to_one
  sql_on: ${user_order_facts.user_id} = ${order_items.user_id} ;;
}

    
join: products {
    type: left_outer
  relationship: many_to_one
  sql_on: ${products.id} = ${inventory_items.product_id} ;;
}

    
join: repeat_purchase_facts {
    relationship: many_to_one
  type: full_outer
  sql_on: ${order_items.order_id} = ${repeat_purchase_facts.order_id} ;;
}

    
join: distribution_centers {
    type: left_outer
  sql_on: ${distribution_centers.id} = ${inventory_items.product_distribution_center_id} ;;
  relationship: many_to_one
}

}
