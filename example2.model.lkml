
connection: "disco-parsec" 
include: "['*.view', '*.dashboard']"
datagroup: sweet_datagroup {  max_cache_age: "1 hour"  sql_trigger: SELECT CURRENT_DATE() ;; } 


explore: trip {
  join: test123 {} 
}
explore: station_weather_forecast {
  join: station { relationship: one_to_many type: cross } 
  hidden: yes
  from: weather_forecast
  view_name: weather_forecast 
}
explore: station_forecasting {
  join: trip_end_count_prediction { relationship: one_to_one  sql_on: ${trip_start_count_prediction.forecast_date} = ${trip_end_count_prediction.forecast_date}
    AND ${trip_start_count_prediction.station_id} = ${trip_end_count_prediction.station_id} ;; }
  join: station { relationship: many_to_one  sql_on: ${station.station_id} = ${trip_start_count_prediction.station_id} ;; } 
  view_name: trip_start_count_prediction
  from: trip_start_count_prediction 
}