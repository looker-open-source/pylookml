include: "/views/**/*.view" # include all the views


########################################################################################
# Cohort Data Tool Explore
# dynamic join on cohort size depending on what cohort is selected by the user
########################################################################################
explore: cohorts {
  hidden: yes
  label: "Cohort Data Tool"
  view_name: cohort_size
  join: users {
    fields: [users.id, users.name, users.first_name, users.last_name, users.email, users.age, users.created_date, users.gender, users.traffic_source, users.count]
    type: left_outer
    relationship: many_to_one
    sql_on:
      CASE
        WHEN {% parameter cohort_size.cohort_filter %} = 'User Signup Month'
          THEN ${users.created_month} = ${cohort_size.cohort}
        WHEN {% parameter cohort_size.cohort_filter %} = 'Gender'
          THEN ${users.gender} = ${cohort_size.cohort}
        WHEN {% parameter cohort_size.cohort_filter %} = 'Age Group'
          THEN ${users.age_tier} = ${cohort_size.cohort}
        WHEN {% parameter cohort_size.cohort_filter %} = 'Traffic Source'
          THEN ${users.traffic_source} = ${cohort_size.cohort}
        ELSE ${users.created_month} = ${cohort_size.cohort}
      END
    ;;
  }
  join: order_items {
    from: order_items_cohorts
    fields: [order_items.id, order_items.order_id, order_items.created_date, order_items.total_sale_price, order_items.months_since_signup]
    type: left_outer
    relationship: one_to_many
    sql_on: ${users.id} = ${order_items.user_id} ;;
  }
}

########################################################################################
# Define Cohort Size
# dynamically swap grouping for user signup month, gender, age group, traffic source
########################################################################################

view: cohort_size {
  view_label: "Cohort"
  derived_table: {
    sql: SELECT
      CASE
        WHEN {% parameter cohort_filter %} = 'User Signup Month'
          THEN cast(DATE_TRUNC(date(users.created_at), MONTH) as string)
        WHEN {% parameter cohort_filter %} = 'Gender'
          THEN users.gender
        WHEN {% parameter cohort_filter %} = 'Traffic Source'
          THEN users.traffic_source
        WHEN {% parameter cohort_filter %} = 'Age Group'
          THEN
            (CASE
              WHEN users.age  < 0 THEN 'Below 0'
              WHEN users.age  >= 0 AND users.age  < 10 THEN '0 to 9'
              WHEN users.age  >= 10 AND users.age  < 20 THEN '10 to 19'
              WHEN users.age  >= 20 AND users.age  < 30 THEN '20 to 29'
              WHEN users.age  >= 30 AND users.age  < 40 THEN '30 to 39'
              WHEN users.age  >= 40 AND users.age  < 50 THEN '40 to 49'
              WHEN users.age  >= 50 AND users.age  < 60 THEN '50 to 59'
              WHEN users.age  >= 60 AND users.age  < 70 THEN '60 to 69'
              WHEN users.age  >= 70 THEN '70 or Above'
              ELSE 'Undefined'
            END)
      ELSE cast(DATE_TRUNC(date(users.created_at), MONTH) as string)
      END AS cohort,
      COUNT(DISTINCT users.id ) AS cohort_size
      FROM ecomm.users AS users
      GROUP BY 1
       ;;
  }

  parameter: cohort_filter {
    label: "Cohort Picker"
    description: "Choose a cohort"
    allowed_value: { value: "User Signup Month" }
    allowed_value: { value: "Gender" }
    allowed_value: { value: "Age Group" }
    allowed_value: { value: "Traffic Source" }
  }

  parameter: metric_filter {
    label: "Metric Picker"
    description: "Choose a metric"
    allowed_value: { value: "User Retention" }
    allowed_value: { value: "Average Orders per User" }
    allowed_value: { value: "Average Spend per User" }
#     allowed_value: { value: "Cumulative Spend" }
  }

  measure: cohort_size {
    type: sum
    sql: ${TABLE}.cohort_size ;;
    drill_fields: [users.id, users.name, users.email, users.age, users.created_date, users.count]
  }

  dimension: cohort {
    description: "Use in conjuction with the Cohort Picker"
    primary_key: yes
    type: string
    sql: ${TABLE}.cohort ;;
    label_from_parameter: cohort_filter
  }

  measure: metric {
    type: number
    description: "Use in conjuction with the Metric Picker"
    sql: CASE
          WHEN {% parameter metric_filter %} = 'User Retention' THEN trunc(${percent_user_retention})
          WHEN {% parameter metric_filter %} = 'Average Orders per User' THEN round(${average_orders_per_user},2)
          WHEN {% parameter metric_filter %} = 'Average Spend per User' THEN trunc(${average_spend_per_user})
          ELSE NULL
        END ;;
#     html:  {% if metric_name._value contains 'User Retention' %}
#             {{ linked_value }}{{ format_symbol._value }}
#           {% else %}
#             {{ format_symbol._value }}{{ linked_value }}
#           {% endif %} ;;
      drill_fields: [cohort_size, percent_user_retention, users.count, average_orders_per_user, average_spend_per_user]
      label_from_parameter: metric_filter
    }

    measure: percent_user_retention {
      view_label: "Users"
      description: "number of active users / number of users in the cohort (use with months since signup dimension)"
      type: number
      sql: round(100.0 * ${users.count} / nullif(${cohort_size},0),2) ;;
      value_format: "0.00\%"
      drill_fields: [users.count, cohort_size, percent_user_retention]
    }

    measure: average_spend_per_user {
      view_label: "Order Items"
      type: number
      value_format_name: usd
      sql: 1.0 * ${order_items.total_sale_price} / NULLIF(${users.count},0) ;;
      drill_fields: [order_items.id, order_items.order_id, order_items.created_date, order_items.total_sale_price, users.email]
    }

    measure: average_orders_per_user {
      view_label: "Order Items"
      type: number
      value_format_name: usd
      sql: 1.0 * ${order_items.order_count} / NULLIF(${users.count},0) ;;
      drill_fields: [users.email, order_items.order_count]
    }

#   measure: cumulative_spend {
#     view_label: "Order Items"
#     type: running_total
#     direction: "column"
#     value_format_name: usd
#     sql: ${order_items.total_sale_price} ;;
#     drill_fields: [order_items.id, order_items.order_id, order_items.created_date, order_items.total_sale_price, users.email]
#   }


################################################################
# Used for dynamically applying a format to the metric parameter
################################################################

    dimension: metric_name {
      hidden: yes
      type: string
      sql: CASE
          WHEN {% parameter metric_filter %} = 'User Retention' THEN 'User Retention'
          WHEN {% parameter metric_filter %} = 'Average Orders per User' THEN 'Average Orders per User'
          WHEN {% parameter metric_filter %} = 'Average Spend per User' THEN 'Average Spend per User'
          WHEN {% parameter metric_filter %} = 'Cumulative Spend' THEN 'Cumulative Spend'
          ELSE NULL
        END ;;
    }

    dimension: format_symbol {
      hidden: yes
      sql:
        CASE
          WHEN ${metric_name} = 'User Retention' THEN '%'
          WHEN ${metric_name} = 'Average Spend per User' THEN '$'
          WHEN ${metric_name} = 'Cumulative Spend' THEN '$'
          ELSE NULL
        END ;;
    }
  }


################################################################
# Group 'months since signup' under Order Items
################################################################


  view: order_items_cohorts {
    extends: [order_items]

    dimension: months_since_signup {
      view_label: "Order Items"
      description: "Months an order occurred since the user first signed up"
      type: number
      sql: DATE_DIFF(date(${users.created_raw}), date(${created_raw}), MONTH) ;;
    }
  }
