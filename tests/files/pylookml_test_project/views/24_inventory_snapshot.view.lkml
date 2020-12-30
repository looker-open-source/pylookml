view: inventory_snapshot {
  derived_table: {
    datagroup_trigger: ecommerce_etl
    sql: with calendar as
      (
      select distinct created_at as snapshot_date
        from looker-private-demo.ecomm.inventory_items
      )

      select
        inventory_items.product_id
        ,calendar.snapshot_date
        ,count(*) as number_in_stock
      from looker-private-demo.ecomm.inventory_items
         join calendar
          on inventory_items.created_at <= calendar.snapshot_date
          and (date(inventory_items.sold_at) >= calendar.snapshot_date OR inventory_items.sold_at is null)
        group by 1,2;;
  }

  dimension: product_id {
    type: number
    sql: ${TABLE}.product_id ;;
  }

  dimension: snapshot_date {
    type: date
    sql:  cast(${TABLE}.snapshot_date as timestamp) ;;
  }

  dimension: number_in_stock {
    type: number
    hidden: yes
    sql: ${TABLE}.number_in_stock ;;
  }

  measure: total_in_stock {
    type: sum
    sql: ${number_in_stock} ;;
  }

  measure: stock_coverage_ratio {
    type: number
    sql: 1.0 * ${total_in_stock} / (11.0*nullif(${trailing_sales_snapshot.sum_trailing_28d_sales},0)) ;;
    value_format_name: decimal_2
  }

  measure: sum_stock_yesterday {
    type: sum
    hidden: yes
    sql: ${number_in_stock} ;;
    filters: {
      field: snapshot_date
      value: "yesterday"
    }
  }

  measure: sum_stock_last_wk {
    type: sum
    hidden: yes
    sql: ${number_in_stock} ;;
    filters: {
      field: snapshot_date
      value: "8 days ago for 1 day"
    }
  }

  measure: stock_coverage_ratio_yday {
    type: number
    view_label: "Stock Ratio Changes"
    sql: 1.0 * ${sum_stock_yesterday} / (11*nullif(${trailing_sales_snapshot.sum_trailing_28d_sales_yesterday},0)) ;;
    value_format_name: decimal_2
  }

  measure: stock_coverage_ratio_last_wk {
    type: number
    view_label: "Stock Ratio Changes"
    sql: 1.0 * ${sum_stock_last_wk} / nullif(${trailing_sales_snapshot.sum_trailing_28d_sales_last_wk},0) ;;
    value_format_name: decimal_2
  }

  measure: wk_to_wk_change_coverage {
    label: "WoW Change - Coverage Ratio"
    view_label: "Stock Ratio Changes"
    sql: round(100*(${stock_coverage_ratio_yday}-${stock_coverage_ratio_last_wk}),1) ;;
    value_format_name: decimal_1
#     value_format: "# 'bp'"
  }

  set: detail {
    fields: [product_id, snapshot_date, number_in_stock]
  }
}
