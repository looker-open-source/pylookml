connection: "snowflake"
label: "1) eCommerce with Event Data"
include: "*.view"

    datagroup: mydatagroup { sql_trigger: select current_date ;;
  label: "Daily"
  description: "Should fire daily just afte midnight UTC" }
    datagroup: mydatagroup2 { sql_trigger: select convert_tz(current_date, 'America/Los_Angeles') ;;
  label: "Daily"
  description: "Should fire daily just afte midnight pacific" }

    named_value_format: euro_in_thousands { value_format: "\"€\"0.000,\" K\""
  strict_value_format: yes }
    named_value_format: euro_in_millions { value_format: "\"€\"0.0000,\" M\""
  strict_value_format: yes }

    map_layer: neighborhoods { file: "my_neighborhoods.json" }
    map_layer: cities { file: "cities.json" }

    access_grant: abc { allowed_values: [
    "a",
    "b",
    "c",
    ]
  user_attribute: abc }
    access_grant: xyz { allowed_values: [
    "x",
    "y",
    "z",
    ]
  user_attribute: abc }

 explore: order_items { 
  label: "(1) Orders, Items and Users"
  view_name: order_items 
  join: order_facts { 
    required_access_grants: [ abc,] 
    type: left_outer
    view_label: "Orders"
    relationship: many_to_one
    sql_on: ${order_facts.order_id} = ${order_items.order_id} ;; }
  join: inventory_items { 
    type: full_outer
    relationship: one_to_one
    sql_on: ${inventory_items.id} = ${order_items.inventory_item_id} ;; }
  join: users { 
    type: left_outer
    relationship: many_to_one
    sql_on: ${order_items.user_id} = ${users.id} ;; }
  join: user_order_facts { 
    view_label: "Users"
    type: left_outer
    relationship: many_to_one
    sql_on: ${user_order_facts.user_id} = ${order_items.user_id} ;; }
  join: products { 
    type: left_outer
    relationship: many_to_one
    sql_on: ${products.id} = ${inventory_items.product_id} ;; }
  join: repeat_purchase_facts { 
    relationship: many_to_one
    type: full_outer
    sql_on: ${order_items.order_id} = ${repeat_purchase_facts.order_id} ;; }
  join: distribution_centers { 
    type: left_outer
    sql_on: ${distribution_centers.id} = ${inventory_items.product_distribution_center_id} ;;
    relationship: many_to_one } }


view: order_items {
  sql_table_name: ecomm.order_items ;;
#  parameter: foo {   allowed_value: { label: "foobar"
#  value: "bar" }
# allowed_value: { label: "x"
#  value: "x" } }
  filter: cohort_by { 
    type: string
    hidden: yes
    suggestions: [
    "Week",
    "Month",
    "Quarter",
    "Year",
    ] }
  filter: metric { 
    type: string
    hidden: yes
    suggestions: [
    "Order Count",
    "Gross Margin",
    "Total Sales",
    "Unique Users",
    ] }
  dimension: days_since_sold {   hidden: yes
    sql: datediff('day',${created_raw},CURRENT_DATE) ;; }
  dimension: days_to_process {   type: number
    sql: CASE
        WHEN ${status} = 'Processing' THEN DATEDIFF('day',${created_raw},current_date)*1.0
        WHEN ${status} IN ('Shipped', 'Complete', 'Returned') THEN DATEDIFF('day',${created_raw},${shipped_raw})*1.0
        WHEN ${status} = 'Cancelled' THEN NULL
      END ;; }
  dimension: days_until_next_order { 
    type: number
    view_label: "Repeat Purchase Facts"
    sql: DATEDIFF('day',${created_raw},${repeat_purchase_facts.next_order_raw}) ;; }
  dimension: gross_margin { 
    type: number
    value_format_name: usd
    sql: ${sale_price} - ${inventory_items.cost} ;;
    html: {{sale_price._value}} ;; }
  dimension: id { 
    primary_key: yes
    type: number
    sql: ${TABLE}.test_sql_change ;;
    required_access_grants: [ abc,] 
    tags: [
    "a",
    "b",
    "c",
    ]
    suggestions: [
    "suggestion1",
    "suggestion2",
    ]
    
action: { label: "Send this to slack channel"
  url: "https://hooks.zapier.com/hooks/catch/1662138/tvc3zj/"
  
param: { name: "user_dash_link"
  value: "https://demo.looker.com/dashboards/160?Email={{ users.email._value}}" }
  
form_param: { name: "Message"
  type: textarea
  default: "Hey,
        Could you check out order #{{value}}. It's saying its {{status._value}},
        but the customer is reaching out to us about it.
        ~{{ _user_attributes.first_name}}" }
form_param: { name: "Recipient"
  type: select
  default: "zevl"
  
option: { name: "zevl"
  label: "Zev" }
option: { name: "slackdemo"
  label: "Slack Demo User" } }
form_param: { name: "Channel"
  type: select
  default: "cs"
  
option: { name: "cs"
  label: "Customer Support" }
option: { name: "general"
  label: "General" } } }
action: { label: "Create Order Form"
  url: "https://hooks.zapier.com/hooks/catch/2813548/oosxkej/"
  
form_param: { name: "Order ID"
  type: string
  default: "{{ order_id._value }}" }
form_param: { name: "Name"
  type: string
  default: "{{ users.name._value }}" }
form_param: { name: "Email"
  type: string
  default: "{{ _user_attributes.email }}" }
form_param: { name: "Item"
  type: string
  default: "{{ products.item_name._value }}" }
form_param: { name: "Price"
  type: string
  default: "{{ order_items.sale_price._rendered_value }}" }
form_param: { name: "Comments"
  type: string
  default: " Hi {{ users.first_name._value }}, thanks for your business!" } } }
  dimension: inventory_item_id { 
    type: number
    hidden: yes
    sql: ${TABLE}.inventory_item_id ;; }
  dimension: is_returned {   type: yesno
    sql: ${returned_raw} IS NOT NULL ;; }
  dimension: item_gross_margin_percentage { 
    type: number
    value_format_name: percent_2
    sql: 1.0 * ${gross_margin}/NULLIF(${sale_price},0) ;; }
  dimension: item_gross_margin_percentage_tier { 
    type: tier
    sql: 100*${item_gross_margin_percentage} ;;
    tiers: [ 0, 10, 20, 30, 40, 50, 60, 70, 80, 90,] 
    style: interval }
  dimension: months_since_signup { 
    view_label: "Orders"
    type: number
    sql: DATEDIFF('month',${users.created_raw},${created_raw}) ;; }
  dimension: periods_as_customer { 
    type: number
    hidden: yes
    sql: DATEDIFF({% parameter cohort_by %}, ${user_order_facts.first_order_date}, ${user_order_facts.latest_order_date}) ;; }
  dimension: repeat_orders_within_30d { 
    type: yesno
    view_label: "Repeat Purchase Facts"
    sql: ${days_until_next_order} <= 30 ;; }
  dimension: reporting_period {   group_label: "Order Date"
    sql: CASE
        WHEN date_part('year',${created_raw}) = date_part('year',current_date)
        AND ${created_raw} < CURRENT_DATE
        THEN 'This Year to Date'
  WHEN date_part('year',${created_raw}) + 1 = date_part('year',current_date)
        AND date_part('dayofyear',${created_raw}) <= date_part('dayofyear',current_date)
        THEN 'Last Year to Date'

      END ;; }
  dimension: sale_price { 
    type: number
    value_format_name: usd
    sql: ${TABLE}.sale_price ;; }
  dimension: status {   sql: ${TABLE}.status ;; }
  dimension: test_add_dimension {   type: string }
  dimension: time_in_transit {   type: number
    sql: datediff('day',${shipped_raw},${delivered_raw})*1.0 ;; }
  dimension: user_id { 
    type: number
    hidden: yes
    sql: ${TABLE}.user_id ;; }
  dimension_group: created { 
    type: time
    timeframes: [ time, hour, date, week, month, year, hour_of_day, day_of_week, month_num, month_name, raw, week_of_year,] 
    sql: ${TABLE}.created_at ;; }
  dimension_group: delivered { 
    type: time
    timeframes: [ date, week, month, raw,] 
    sql: ${TABLE}.delivered_at ;; }
  dimension_group: first_order_period { 
    type: time
    timeframes: [ date,] 
    hidden: yes
    sql: CAST(DATE_TRUNC({% parameter cohort_by %}, ${user_order_facts.first_order_date}) AS DATE) ;; }
  dimension_group: returned { 
    type: time
    timeframes: [ time, date, week, month, raw,] 
    sql: ${TABLE}.returned_at ;; }
  dimension_group: shipped { 
    type: time
    timeframes: [ date, week, month, raw,] 
    sql: ${TABLE}.shipped_at ;; }
  measure: 30_day_repeat_purchase_rate { 
    description: "The percentage of customers who purchase again within 30 days"
    view_label: "Repeat Purchase Facts"
    type: number
    value_format_name: percent_1
    sql: 1.0 * ${count_with_repeat_purchase_within_30d} / NULLIF(${count},0) ;;
    drill_fields: [ products.brand, order_count, count_with_repeat_purchase_within_30d, 30_day_repeat_purchase_rate,]  }
  measure: average_days_to_process { 
    type: average
    value_format_name: decimal_2
    sql: ${days_to_process} ;; }
  measure: average_gross_margin { 
    type: average
    value_format_name: usd
    sql: ${gross_margin} ;;
    drill_fields: [ detail*,]  }
  measure: average_sale_price { 
    type: average
    value_format_name: usd
    sql: ${sale_price} ;;
    drill_fields: [ detail*,]  }
  measure: average_shipping_time { 
    type: average
    value_format_name: decimal_2
    sql: ${time_in_transit} ;; }
  measure: average_spend_per_user { 
    type: number
    value_format_name: usd
    sql: 1.0 * ${total_sale_price} / NULLIF(${users.count},0) ;;
    drill_fields: [ detail*,]  }
  measure: cohort_values_0 { 
    type: count_distinct
    hidden: yes
    sql: CASE WHEN {% parameter metric %} = 'Order Count' THEN ${id}
        WHEN {% parameter metric %} = 'Unique Users' THEN ${users.id}
        ELSE null
      END ;; }
  measure: cohort_values_1 { 
    type: sum
    hidden: yes
    sql: CASE WHEN {% parameter metric %} = 'Gross Margin' THEN ${gross_margin}
        WHEN {% parameter metric %} = 'Total Sales' THEN ${sale_price}
        ELSE 0
      END ;; }
  measure: count { 
    type: count_distinct
    sql: ${id} ;;
    drill_fields: [ detail*,]  }
  measure: count_last_28d { 
    label: "Count Sold in Trailing 28 Days"
    type: count_distinct
    sql: ${id} ;;
    hidden: yes
    
filters: {     field: created_date
  value: "28 days" } }
  measure: count_with_repeat_purchase_within_30d { 
    type: count_distinct
    sql: ${id} ;;
    view_label: "Repeat Purchase Facts"
    
filters: {     field: repeat_orders_within_30d
  value: "Yes" } }
  measure: first_purchase_count { 
    view_label: "Orders"
    type: count_distinct
    sql: ${order_id} ;;
    
filters: {     field: order_facts.is_first_purchase
  value: "Yes" }
    drill_fields: [ user_id, order_id, created_date, users.traffic_source,] 
    
link: { label: "New User's Behavior by Traffic Source"
  url: "
      {% assign vis_config = '{
      \"type\": \"looker_column\",
      \"show_value_labels\": true,
      \"y_axis_gridlines\": true,
      \"show_view_names\": false,
      \"y_axis_combined\": false,
      \"show_y_axis_labels\": true,
      \"show_y_axis_ticks\": true,
      \"show_x_axis_label\": false,
      \"value_labels\": \"legend\",
      \"label_type\": \"labPer\",
      \"font_size\": \"13\",
      \"colors\": [
      \"#1ea8df\",
      \"#a2dcf3\",
      \"#929292\"
      ],
      \"hide_legend\": false,
      \"y_axis_orientation\": [
      \"left\",
      \"right\"
      ],
      \"y_axis_labels\": [
      \"Average Sale Price ($)\"
      ]
      }' %}
      {{ hidden_first_purchase_visualization_link._link }}&vis_config={{ vis_config | encode_uri }}&sorts=users.average_lifetime_orders+descc&toggle=dat,pik,vis&limit=5000" } }
  measure: hidden_first_purchase_visualization_link { 
    hidden: yes
    view_label: "Orders"
    type: count_distinct
    sql: ${order_id} ;;
    
filters: {     field: order_facts.is_first_purchase
  value: "Yes" }
    drill_fields: [ users.traffic_source, user_order_facts.average_lifetime_revenue, user_order_facts.average_lifetime_orders,]  }
  measure: median_sale_price { 
    type: median
    value_format_name: usd
    sql: ${sale_price} ;;
    drill_fields: [ detail*,]  }
  measure: order_count { 
    view_label: "Orders"
    type: count_distinct
    drill_fields: [ detail*,] 
    sql: ${order_id} ;; }
  measure: return_rate { 
    type: number
    value_format_name: percent_2
    sql: 1.0 * ${returned_count} / nullif(${count},0) ;; }
  measure: returned_count { 
    type: count_distinct
    sql: ${id} ;;
    
filters: {     field: is_returned
  value: "yes" }
    drill_fields: [ detail*,]  }
  measure: returned_total_sale_price { 
    type: sum
    value_format_name: usd
    sql: ${sale_price} ;;
    
filters: {     field: is_returned
  value: "yes" } }
  measure: total_gross_margin { 
    type: sum
    value_format_name: usd
    sql: ${gross_margin} ;;
    drill_fields: [ detail*,]  }
  measure: total_gross_margin_percentage { 
    type: number
    value_format_name: percent_2
    sql: 1.0 * ${total_gross_margin}/ NULLIF(${total_sale_price},0) ;; }
  measure: total_sale_price { 
    type: sum
    value_format_name: usd
    sql: ${sale_price} ;;
    drill_fields: [ detail*,]  }
  measure: values { 
    type: number
    hidden: yes
    sql: ${cohort_values_0} + ${cohort_values_1} ;; }
  
    set: detail { fields: [ id, order_id, status, created_date, sale_price, products.brand, products.item_name, users.portrait, users.name, users.email, user_order_facts.phone_number,]  }
    set: return_detail { fields: [ id, order_id, status, created_date, returned_date, sale_price, products.brand, products.item_name, users.portrait, users.name, users.email,]  }}
