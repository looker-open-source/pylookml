view: cool {


#this is bar
dimension: bar {
  type: string
}


dimension: foo {
  sql: COALESCE(${TABLE}.id,0) ;;
  tags: [
    "Generated Code",
    ]
}


dimension_group: foo_date {
  timeframes: [raw
  ,year
  ,quarter
  ,month
  ,week
  ,date
  ,day_of_week
  ,hour
  ,hour_of_day
  ,minute
  ,time
  ,time_of_day]
  type: time
  sql: ${TABLE}.`` ;;
}


filter: foo_filter {
  
}


dimension: hugo {
  link: {
    label: "Website"
    url: "http://www.google.com/search?q={{ value | encode_uri }}+clothes&btnI"
    icon_url: "http://www.google.com/s2/favicons?domain=www.{{ value | encode_uri }}.com"
    }
}


#Auto Generated -- Dont touch
dimension: id {
  type: string
  sql: COALESCE(${TABLE}.id,0) ;;
  tags: [
    "Generated Code",
    ]
}


dimension: tst {
  
}

}
