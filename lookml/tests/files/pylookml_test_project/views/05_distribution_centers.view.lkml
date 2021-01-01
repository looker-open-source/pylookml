view: distribution_centers {
  sql_table_name: looker-private-demo.ecomm.distribution_centers ;;
  dimension: location {
    type: location
    sql_latitude: ${TABLE}.latitude ;;
    sql_longitude: ${TABLE}.longitude ;;
  }

  dimension: latitude {
    sql: ${TABLE}.latitude ;;
    hidden: yes
  }

  dimension: longitude {
    sql: ${TABLE}.longitude ;;
    hidden: yes
  }

  dimension: id {
    type: number
    primary_key: yes
    sql: ${TABLE}.id ;;
  }

  dimension: name {
    sql: ${TABLE}.name ;;
  }
}
