import lookml, lang
import unittest
import lkml as lkml
from pprint import pprint
import file

# TODO P1 Looping through view.views poduces a [None]
# Explore source??

class test_view(unittest.TestCase):
  def setUp(self):
      self.view = file.File('tests/files/basic_parsing/basic.view.lkml')

  def test_walking(self):
    for explore in self.view.explores:
      assert explore.name in ['basic']
      assert type(explore.join) == lookml.prop_named_construct

  def test_walk_explore(self):
    explore = self.view.explores.basic
    assert type(explore.join.cool) == lookml.prop_named_construct_single

  def test_walk_join(self):
    join = self.view.explores.basic.join.cool
    assert type(join) == lookml.prop_named_construct_single

    assert type(join.relationship) == lookml.prop_options
    assert join.relationship.value == 'many_to_one'
    
    assert type(join.type) == lookml.prop_options
    assert join.type.value == 'left_outer'
    
    assert type(join.sql_on) == lookml.prop_sql
    assert join.sql_on.value == '${basic.cool_id} = ${cool.basic_id}'
    # assert join.from == lookml.prop.string_unquoted

  def test_walk_view(self):
    view = self.view.views.basic
    assert type(view.extends) == lookml.prop_list_unquoted
    assert view.extends.value == ['base']

    assert type(view.extension) == lookml.prop_options
    assert view.extension.value == 'required'

    assert type(view.final) == lookml.prop_yesno
    assert view.final.value == 'no'

    assert type(view.label) == lookml.prop_string
    assert view.label.value == 'basic'

    assert type(view.view_label) == lookml.prop_string
    assert view.view_label.value == 'basic'

    assert type(view.required_access_grants) == lookml.prop_list_unquoted
    assert view.required_access_grants.value == ['a', 'b', 'c']

    assert type(view.suggestions) == lookml.prop_yesno
    assert view.suggestions.value == 'yes'

    assert type(view.derived_table) == lookml.prop_anonymous_construct

    for dim in view._dims():
      assert dim.name in ['foo', 'bar']

    assert type(view.transaction) == lookml.Dimension_Group

    for param in view._params():
      assert param.name in ['myparam']

    for measure in view._measures():
      assert measure.name in ['sum_foo', 'sum_bar']

  def test_walk_measure(self):
    measure = self.view.views.basic.sum_foo
    assert type(measure) == lookml.Measure
    assert measure.name == 'sum_foo'
    
    assert type(measure.type) == lookml.prop_options
    assert measure.type.value == 'sum'

    assert type(measure.sql) == lookml.prop_sql
    assert measure.sql.value == '${foo}'

    assert type(measure.filters) == lookml.prop_filters

  def test_walk_filters(self):
    filter = self.view.views.basic.sum_foo.filters.foo
    filter2 = self.view.views.basic.sum_bar.filters.foo

    assert type(filter) == lookml.flt
    assert filter.value == '%cool%'

    assert type(filter2) == lookml.flt
    assert filter2.value == '%cool%'

  def test_walk_dimension_group(self):
    dg = self.view.views.basic.transaction

    assert type(dg) == lookml.Dimension_Group
    assert dg.name == 'transaction'

    assert type(dg.type) == lookml.prop_options
    assert dg.type.value == 'time'

    assert type(dg.tags) == lookml.prop_list_quoted
    assert dg.tags.value == ['tag1', 'tag2', 'tag3', 'tag4']

    assert type(dg.timeframes) == lookml.prop_list_unquoted
    assert dg.timeframes.value == ['raw', 'time', 'date', 'week', 'month',
                                  'quarter', 'year', 'week_of_year', 'month_num']

    assert type(dg.sql) == lookml.prop_sql
    assert dg.sql.value == '${TABLE}.transaction_timestamp'

  def test_walk_dimension(self):
    dimension = self.view.views.basic.foo
    assert type(dimension) == lookml.Dimension

    assert type(dimension.type) == lookml.prop_options
    assert dimension.type.value == 'string'

    assert type(dimension.style) == lookml.prop_options
    assert dimension.style.value == 'classic'

    assert type(dimension.sql) == lookml.prop_sql
    assert dimension.sql.value == '${TABLE}.foo'

    assert type(dimension.link) == lookml.prop_anonymous_construct_plural