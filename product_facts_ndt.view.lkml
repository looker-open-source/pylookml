view: product_facts_ndt {
derived_table: {
explore_source: order_items  {
    column: id { field: products.id}
    column: total_value { field: order_items.total_value}
    
    }
}

dimension: id {
    sql: ${TABLE}.`id` ;;
    type: string
}

    
dimension: total_value {
    sql: ${TABLE}.`total_value` ;;
    type: string
}

    
measure: total_total_value {
    sql: ${total_value} ;;
    type: sum
}

}
