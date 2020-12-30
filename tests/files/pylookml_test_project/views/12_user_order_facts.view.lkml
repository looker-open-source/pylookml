view: user_order_facts {
  derived_table: {
    sql:
    SELECT
        user_id
        , COUNT(DISTINCT order_id) AS lifetime_orders
        , SUM(sale_price) AS lifetime_revenue
        , CAST(MIN(created_at)  AS TIMESTAMP) AS first_order
        , CAST(MAX(created_at)  AS TIMESTAMP)  AS latest_order
        , COUNT(DISTINCT FORMAT_TIMESTAMP('%Y%m', created_at))  AS number_of_distinct_months_with_orders
        --, FIRST_VALUE(CONCAT(uniform(2, 9, random(1)),uniform(0, 9, random(2)),uniform(0, 9, random(3)),'-',uniform(0, 9, random(4)),uniform(0, 9, random(5)),uniform(0, 9, random(6)),'-',uniform(0, 9, random(7)),uniform(0, 9, random(8)),uniform(0, 9, random(9)),uniform(0, 9, random(10)))) OVER (PARTITION BY user_id ORDER BY user_id) AS phone_number
      FROM looker-private-demo.ecomm.order_items
      GROUP BY user_id
    ;;
    datagroup_trigger: ecommerce_etl
  }

  dimension: user_id {
    primary_key: yes
    hidden: yes
    sql: ${TABLE}.user_id ;;
  }

#   dimension: phone_number {
#     type: string
#     tags: ["phone"]
#     sql: ${TABLE}.phone_number ;;
#   }


  ##### Time and Cohort Fields ######

  dimension_group: first_order {
    type: time
    timeframes: [date, week, month, year]
    sql: ${TABLE}.first_order ;;
  }

  dimension_group: latest_order {
    type: time
    timeframes: [date, week, month, year]
    sql: ${TABLE}.latest_order ;;
  }

  dimension: days_as_customer {
    description: "Days between first and latest order"
    type: number
    sql: TIMESTAMP_DIFF(${TABLE}.latest_order, ${TABLE}.first_order, DAY)+1 ;;
  }

  dimension: days_as_customer_tiered {
    type: tier
    tiers: [0, 1, 7, 14, 21, 28, 30, 60, 90, 120]
    sql: ${days_as_customer} ;;
    style: integer
  }

  ##### Lifetime Behavior - Order Counts ######

  dimension: lifetime_orders {
    type: number
    sql: ${TABLE}.lifetime_orders ;;
  }

  dimension: repeat_customer {
    description: "Lifetime Count of Orders > 1"
    type: yesno
    sql: ${lifetime_orders} > 1 ;;
  }

  dimension: lifetime_orders_tier {
    type: tier
    tiers: [0, 1, 2, 3, 5, 10]
    sql: ${lifetime_orders} ;;
    style: integer
  }

  measure: average_lifetime_orders {
    type: average
    value_format_name: decimal_2
    sql: ${lifetime_orders} ;;
  }

  dimension: distinct_months_with_orders {
    type: number
    sql: ${TABLE}.number_of_distinct_months_with_orders ;;
  }

  ##### Lifetime Behavior - Revenue ######

  dimension: lifetime_revenue {
    type: number
    value_format_name: usd
    sql: ${TABLE}.lifetime_revenue ;;
  }

  dimension: lifetime_revenue_tier {
    type: tier
    tiers: [0, 25, 50, 100, 200, 500, 1000]
    sql: ${lifetime_revenue} ;;
    style: integer
  }

  measure: average_lifetime_revenue {
    type: average
    value_format_name: usd
    sql: ${lifetime_revenue} ;;
  }
}
