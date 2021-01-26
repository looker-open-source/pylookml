include: "/models/**/pylookml_testing.model.lkml"
view: order_facts {
  derived_table: {
    explore_source: order_items {
      column: order_id {field: order_items.order_id_no_actions }
      column: items_in_order { field: order_items.count }
      column: order_amount { field: order_items.total_sale_price }
      column: order_cost { field: inventory_items.total_cost }
      column: user_id {field: order_items.user_id }
      column: created_at {field: order_items.created_raw}
      column: order_gross_margin {field: order_items.total_gross_margin}
      derived_column: order_sequence_number {
        sql: RANK() OVER (PARTITION BY user_id ORDER BY created_at) ;;
      }
    }
    datagroup_trigger: ecommerce_etl
  }

  dimension: order_id {
    type: number
    hidden: yes
    primary_key: yes
    sql: ${TABLE}.order_id ;;
  }

  dimension: items_in_order {
    type: number
    sql: ${TABLE}.items_in_order ;;
  }

  dimension: order_amount {
    type: number
    value_format_name: usd
    sql: ${TABLE}.order_amount ;;
  }

  dimension: order_cost {
    type: number
    value_format_name: usd
    sql: ${TABLE}.order_cost ;;
  }

  dimension: order_gross_margin {
    type: number
    value_format_name: usd
  }

  dimension: order_sequence_number {
    type: number
    sql: ${TABLE}.order_sequence_number ;;
  }

  dimension: is_first_purchase {
    type: yesno
    sql: ${order_sequence_number} = 1 ;;
  }
}
