view: foo {
    sql_table_name: public.foo ;;
    dimension: foo { sql: ${TABLE}.foo;; type: number }
    dimension: bar { sql: ${TABLE}.bar ;; }
    dimension: baz {
        type: string
        sql: ${TABLE}.baz ;;
        html: {{ rendered_value }};;
    }
    measure: count_foo {
        type: count
        sql: ${foo} ;;
        value_format_name: usd
        html: {{ rendered_value }};;
    }
    measure: sum_foo {
        type: sum
        sql: ${foo} ;;
    }
}