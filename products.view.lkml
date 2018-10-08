view: products {


dimension: id {
    sql: ${TABLE}.`id` ;;
    type: string
}

    
dimension: name {
    sql: ${TABLE}.`name` ;;
    type: string
}

}
