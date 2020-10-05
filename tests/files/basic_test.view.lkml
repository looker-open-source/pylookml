view: cool {
    extends:[cool1]
    sql_table_name: public.test ;;

    dimension: foo {
        type: string
        sql: ${TABLE}.foo ;;
    }
    dimension: bar {
        type: number
        sql: ${TABLE}.number ;;
    }

    filter: myfilt {
        type: string
        sql: 1=1 ;;
    }

  dimension_group: transaction {
    type: time
    tags: ["foo","cool","data"]
    timeframes: [
      raw,
      time,
      date,
      week,
      month,
      quarter,
      year,
      week_of_year,
      month_num
    ]
    sql: ${TABLE}.transaction_timestamp ;;
  }

    measure: sum_foo {
        type: sum
        sql: ${foo} ;;
        filters: [foo:"%cool%", bar:"%great%", baz:"wow",car:"foo"]
    }
    measure: sum_bar {
        type: sum
        sql: ${bar} ;;
        filters: { field:foo value:"%cool%" }
        filters: { field:bar value:"%great%" }
    }

}