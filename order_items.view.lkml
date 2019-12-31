view: order_items {
sql_table_name: `public.order_items` ;;

dimension_group: created_at {
    timeframes: [raw
    ,year
    ,quarter
    ,month
    ,week
    ,date
    ,day_of_week
    ,hour
    ,hour_of_day
    ,minute
    ,time
    ,time_of_day]
    type: time
    sql: ${TABLE}.`created_at` ;;
}

    
dimension: id {
    sql: ${TABLE}.`id` ;;
    type: number
    link: {
    url: "/dashboards/7?brand=cool"
    label: ""
    icon_url: "https://looker.com/favicon.ico"
    }
}

    
dimension: inventory_item_id {
    sql: ${TABLE}.`inventory_item_id` ;;
    type: number
}

    
dimension: value {
    sql: ${TABLE}.`value` ;;
    type: string
}

    
measure: total_value {
    sql: ${value} ;;
    type: sum
}

}
