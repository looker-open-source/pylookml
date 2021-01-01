connection: "disco-parsec"

include: "*.view"
include: "*.dashboard"

datagroup: sweet_datagroup {
  #Rad datagroup, yo!
  max_cache_age: "1 hour"
  sql_trigger: SELECT CURRENT_DATE() ;;
}

explore: trip {
  join: start_station {
    from: station
    relationship: many_to_one
    type: left_outer
    sql_on: ${trip.from_station_id} = ${start_station.station_id};;
  }

  join: end_station {
    from: station
    relationship: many_to_one
    type: left_outer
    sql_on: ${trip.to_station_id} = ${end_station.station_id};;
  }

  join:  daily_weather {
    relationship: many_to_one
    sql_on: ${trip.start_date} = ${daily_weather.weather_date} ;;
  }
  join: trip_count_prediction {
    relationship: many_to_one
    sql_on: ${trip.start_date} = ${trip_count_prediction.start_date} ;;
  }
}

explore: station_weather_forecast {
  #THIS IS JUST TO FEED INTO THE predictions
  hidden: yes
  from: weather_forecast
  view_name: weather_forecast
  join: station {
    relationship: one_to_many
    type: cross
  }
}

explore: station_forecasting {
  view_name: trip_start_count_prediction
  from: trip_start_count_prediction
  join: trip_end_count_prediction {
#     fields: []
  relationship: one_to_one
  sql_on: ${trip_start_count_prediction.forecast_date} = ${trip_end_count_prediction.forecast_date}
    AND ${trip_start_count_prediction.station_id} = ${trip_end_count_prediction.station_id};;
}
join: station {
  relationship: many_to_one
  sql_on: ${station.station_id} = ${trip_start_count_prediction.station_id} ;;
}
}
