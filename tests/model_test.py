import lookml, lang
import unittest
import lkml as lkml
from pprint import pprint
import file



class testModel(unittest.TestCase):
  def setUp(self):
      self.model = file.File('tests/files/basic_parsing/basic.model.lkml')
      self.explore_names = ['trip', 'station_weather_forecast', 'station_forecasting']

  def test_walking(self):
    for explore in self.model:
      assert explore.name in self.model.explores
      assert isinstance(explore.join, lookml.prop_named_construct)

  def test_walk_explore(self):
    explore = self.model.explores.trip
    assert type(explore.join.start_station) == lookml.prop_named_construct_single

    explore2 = self.model.explores.station_weather_forecast
    assert type(explore2.hidden) == lookml.prop_yesno
    assert explore2.hidden.value == 'yes'
    assert type(explore.view_name) == lookml.prop_string_unquoted
    assert explore2.view_name.value == 'weather_forecast'
    
    # assert explore2.from == lookml.prop.string_unquoted

  def test_walk_join(self):
    join = self.model.explores.trip.join.start_station
    assert type(join) == lookml.prop_named_construct_single
    assert type(join.relationship) == lookml.prop_options
    assert join.relationship.value == 'many_to_one'
    assert type(join.type) == lookml.prop_options
    assert join.type.value == 'left_outer'
    assert type(join.sql_on) == lookml.prop_sql
    assert join.sql_on.value == '${trip.from_station_id} = ${start_station.station_id}'
    # assert join.from == lookml.prop.string_unquoted
