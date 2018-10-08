view: inventory_items {
sql_table_name: `public.inventory_items` ;;

dimension: id {
    sql: ${TABLE}.`id` ;;
    type: string
}

    
dimension: product_id {
    sql: ${TABLE}.`product_id` ;;
    type: string
}

}
