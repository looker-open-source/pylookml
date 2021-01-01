view: users {
  sql_table_name: looker-private-demo.ecomm.users ;;

  ## Demographics ##

  dimension: id {
    primary_key: yes
    type: number
    sql: ${TABLE}.id ;;
    tags: ["user_id"]
  }

  dimension: first_name {
    hidden: yes
    sql: CONCAT(UPPER(SUBSTR(${TABLE}.first_name,1,1)), LOWER(SUBSTR(${TABLE}.first_name,2))) ;;

  }

  dimension: last_name {
    hidden: yes
    sql: CONCAT(UPPER(SUBSTR(${TABLE}.last_name,1,1)), LOWER(SUBSTR(${TABLE}.last_name,2))) ;;
  }

  dimension: name {
    sql: concat(${first_name}, ' ', ${last_name}) ;;
  }

  dimension: age {
    type: number
    sql: ${TABLE}.age ;;
  }

  dimension: over_21 {
    type: yesno
    sql:  ${age} > 21;;
  }

  dimension: age_tier {
    type: tier
    tiers: [0, 10, 20, 30, 40, 50, 60, 70]
    style: integer
    sql: ${age} ;;
  }

  dimension: gender {
    sql: ${TABLE}.gender ;;
  }

  dimension: gender_short {
    sql: LOWER(SUBSTR(${gender},1,1)) ;;
  }

  dimension: user_image {
    sql: ${image_file} ;;
    html: <img src="{{ value }}" width="220" height="220"/>;;
  }

  dimension: email {
    sql: ${TABLE}.email ;;
    tags: ["email"]

    link: {
      label: "User Lookup Dashboard"
      url: "/dashboards/ayalascustomerlookupdb?Email={{ value | encode_uri }}"
      icon_url: "http://www.looker.com/favicon.ico"
    }
    action: {
      label: "Email Promotion to Customer"
      url: "https://desolate-refuge-53336.herokuapp.com/posts"
      icon_url: "https://sendgrid.com/favicon.ico"
      param: {
        name: "some_auth_code"
        value: "abc123456"
      }
      form_param: {
        name: "Subject"
        required: yes
        default: "Thank you {{ users.name._value }}"
      }
      form_param: {
        name: "Body"
        type: textarea
        required: yes
        default:
        "Dear {{ users.first_name._value }},

        Thanks for your loyalty to the Look.  We'd like to offer you a 10% discount
        on your next purchase!  Just use the code LOYAL when checking out!

        Your friends at the Look"
      }
    }
    required_fields: [name, first_name]
  }

  dimension: image_file {
    hidden: yes
    sql: concat('https://docs.looker.com/assets/images/',${gender_short},'.jpg') ;;
  }

  ## Demographics ##

  dimension: city {
    sql: ${TABLE}.city ;;
    drill_fields: [zip]
  }

  dimension: state {
    sql: ${TABLE}.state ;;
    map_layer_name: us_states
    drill_fields: [zip, city]
  }

  dimension: zip {
    type: zipcode
    sql: ${TABLE}.zip ;;
  }

  dimension: uk_postcode {
    label: "UK Postcode"
    sql: case when ${TABLE}.country = 'UK' then regexp_replace(${zip}, '[0-9]', '') else null end;;
    map_layer_name: uk_postcode_areas
    drill_fields: [city, zip]
  }

  dimension: country {
    map_layer_name: countries
    drill_fields: [state, city]
    sql: CASE WHEN ${TABLE}.country = 'UK' THEN 'United Kingdom'
           ELSE ${TABLE}.country
           END
       ;;
  }

  dimension: location {
    type: location
    sql_latitude: ${TABLE}.latitude ;;
    sql_longitude: ${TABLE}.longitude ;;
  }

  dimension: approx_latitude {
    type: number
    sql: round(${TABLE}.latitude,1) ;;
  }

  dimension: approx_longitude {
    type: number
    sql:round(${TABLE}.longitude,1) ;;
  }

  dimension: approx_location {
    type: location
    drill_fields: [location]
    sql_latitude: ${approx_latitude} ;;
    sql_longitude: ${approx_longitude} ;;
    link: {
      label: "Google Directions from {{ distribution_centers.name._value }}"
      url: "{% if distribution_centers.location._in_query %}https://www.google.com/maps/dir/'{{ distribution_centers.latitude._value }},{{ distribution_centers.longitude._value }}'/'{{ approx_latitude._value }},{{ approx_longitude._value }}'{% endif %}"
      icon_url: "http://www.google.com/s2/favicons?domain=www.google.com"
    }

  }

  ## Other User Information ##

  dimension_group: created {
    type: time
#     timeframes: [time, date, week, month, raw]
    sql: ${TABLE}.created_at ;;
  }

  dimension: history {
    sql: ${TABLE}.id ;;
    html: <a href="/explore/thelook_event/order_items?fields=order_items.detail*&f[users.id]={{ value }}">Order History</a>
      ;;
  }

  dimension: traffic_source {
    sql: ${TABLE}.traffic_source ;;
  }

  dimension: ssn {
    # dummy field used in next dim, generate 4 random numbers to be the last 4 digits
    hidden: yes
    type: string
    sql: CONCAT(CAST(FLOOR(10*RAND()) AS INT64),CAST(FLOOR(10*RAND()) AS INT64),
      CAST(FLOOR(10*RAND()) AS INT64),CAST(FLOOR(10*RAND()) AS INT64));;
  }

  dimension: ssn_last_4 {
    label: "SSN Last 4"
    description: "Only users with sufficient permissions will see this data"
    type: string
    sql: CASE WHEN '{{_user_attributes["can_see_sensitive_data"]}}' = 'Yes'
                THEN ${ssn}
                ELSE '####' END;;
  }

  ## MEASURES ##

  measure: count {
    type: count
    drill_fields: [detail*]
  }

  measure: count_percent_of_total {
    label: "Count (Percent of Total)"
    type: percent_of_total
    sql: ${count} ;;
    drill_fields: [detail*]
  }

  measure: average_age {
    type: average
    value_format_name: decimal_2
    sql: ${age} ;;
    drill_fields: [detail*]
  }

  set: detail {
    fields: [id, name, email, age, created_date, orders.count, order_items.count]
  }
}
