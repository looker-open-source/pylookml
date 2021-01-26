view: basic {
    extends:[base]
    extension: required
    final: no
    label: "basic"
    view_label: "basic"
    required_access_grants: [a,b,c]
    suggestions: yes
    #sql_table_name: public.test ;;
    derived_table: {
        #sql: select * from public.test ;;
    explore_source: order_items {
      limit: 500
      column: foo_1 {
        field: foo
      }
      column: foo_2 {
        field: foo
      }
      derived_column: foo_3 {
        sql: ${TABLE}.foo ;;
      }
      bind_all_filters: yes
      sorts: [field_name_1: asc, field_name_2: desc]
      bind_filters: {
        from_field: order_items.foo
        to_field: order_items.foo
      }
      bind_filters: {
        from_field: order_items.bar
        to_field: order_items.bar
      }
    }
    }
    dimension: foo {
        type: string
        style: classic
        sql: ${TABLE}.foo ;;
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
    dimension: bar {
        type: number
        sql: ${TABLE}.number ;;
    action: {
      label: "cool"
      url: "http://beeceptor.com/post"
      icon_url: "https://looker.com/favicon.ico"
      form_url: "https://beeceptor.com/post"
    
      param: {
        name: "foo"
        value: "bar"
      }
      form_param: {
        name: "my form param"
        type: select
        label: "My form Param"
        option: {
          name: "cool"
          label: "Cool"
        }
        option: {
          name: "notcool"
          label: "Not Cool"
        }
        description: "Is it cool or not cool?"
        default: "cool"
     }
    }
    }
    filter: myfilt {type: string sql: 1=1 ;;}
  dimension_group: transaction {
    type: time
    tags: ["tag1","tag2","tag3","tag4"]
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
  parameter: myparam {
      type: unquoted
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
    set: set1 {
        fields: [field1, field2, field3 ]
    }
    set: set2 {
        fields: [field4, field5, view2.field6 ]
    }
}
explore: basic {
  join: cool {
    type: left_outer
    sql_on: ${basic.cool_id} = ${cool.basic_id} ;;
    relationship: many_to_one
  }
  aggregate_table: foo {
    query: {
      dimensions: [created_date, users.state]
      measures: [total_sales]
      pivots: [users.age_tier]
      limit:  500
      timezone: Africa/Bamako
    }
    materialization: {
      datagroup_trigger: foo
    }
  }
}