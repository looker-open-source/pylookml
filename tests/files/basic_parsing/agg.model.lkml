connection: "foo"
include: "*.view.lkml"
explore: foo {
    join: test1 {}
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
  aggregate_table: bar {
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