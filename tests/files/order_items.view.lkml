view: order_items {
    sql_table_name: public.order_items ;;
    
    dimension: foo {
        type: string
        sql: ${TABLE}.foo ;;
        value_format_name: usd
        primary_key: yes
        #case: {
        #    when: {
        #        sql: ${bar} > 3 ;;
        #        label: "bar is greater than 3"
        #    }
        #    else: "bar is not greater than 3"
        #}
        link: {
            url: "https://yahoo.com"
            icon_url: "https://yahoo.com/favicon.ico"
            label: "cool"
        }
        link: {
            url: "https://facebook.com"
            icon_url: "https://facebook.com/favicon.ico"
            label: "social"
        }
    }
    dimension: bar {}
    measure: sum_foo {
        type: sum
        sql: ${foo} ;;
    }
    measure: sum_bar {
        type: sum
        sql: ${bar} ;;
    }
    measure: count { type: count }
    dimension_group: created { type: time }
   # set: myset {
   #     fields: [hello]
   # }
   # set: great {
   #     fields: [wawa]
   # }
}