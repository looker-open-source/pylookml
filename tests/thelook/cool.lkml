view: order_items {

dimension: foo_1 {}
filter: woo_1 {}
measure: bar_1 {}
dimension_group: created_date {}

dimension_group: created {
  timeframes: [
    date,
    raw,
    hour_of_day,
    ]
  type: time
  sql: ${TABLE}.`` ;;
}


filter: cool {
  sql: ${TABLE}.id > 5 ;;
  suggestions: [
    "bob",
    "cool",
    ]
}

dimension_group: date {
  timeframes: [
    raw,
    time,
    ]
  type: time
  sql: ${TABLE}.`` ;;
}


dimension: foo {

  tiers: [
    10,
    11,
    12,
    ]
  tags: [
    "very",
    "important",
    "tags",
    ]
}

measure: hidden_first_purchase_visualization_link {
  hidden: yes
  view_label: "Orders"
  type: count_distinct
  sql: ${order_id} ;;
  filters: {
    field: order_facts.is_first_purchase
    value: "Yes"
    }
 filters:  {
    field: order_facts.is_cancelled
    value: "Yes"
    }
  drill_fields: [
    users.traffic_source,
    user_order_facts.average_lifetime_revenue,
    user_order_facts.average_lifetime_orders,
    ]
  tags: [
    "Generated Code",
    ]
}

}






