_allowed_children = \
{
        "model": [
                "access_grant",
                "case_sensitive",
                "connection",
                "datagroup",
                "explore",
                "fiscal_month_offset",
                "include",
                "label",
                "map_layer",
                "named_value_format",
                "persist_for",
                "persist_with",
                "test",
                "view",
                "week_start_day"
        ],
        "explore": [
                "case_sensitive",
                "label",
                "persist_for",
                "persist_with",
                "extends",
                "extension",
                "final",
                "required_access_grants",
                "sql_table_name",
                "view_label",
                "access_filter",
                "aggregate_table",
                "always_filter",
                "always_join",
                "cancel_grouping_fields",
                "conditionally_filter",
                "description",
                "group_label",
                "from",
                "fields",
                "hidden",
                "join",
                "sql_always_where",
                "sql_always_having",
                "tags",
                "view_name",
                "query"
        ],
        "dimension": [
                "case_sensitive",
                "label",
                "drill_fields",
                "required_access_grants",
                "suggestions",
                "view_label",
                "description",
                "group_label",
                "hidden",
                "tags",
                "action",
                "allow_fill",
                "alpha_sort",
                "bypass_suggest_restrictions",
                "can_filter",
                "case",
                "datatype",
                "end_location_field",
                "fanout_on",
                "full_suggestions",
                "group_item_label",
                "html",
                "label_from_parameter",
                "link",
                "map_layer_name",
                "order_by_field",
                "primary_key",
                "required_fields",
                "skip_drill_filter",
                "start_location_field",
                "suggest_persist_for",
                "style",
                "sql",
                "sql_end",
                "sql_start",
                "tiers",
                "sql_longitude",
                "sql_latitude",
                "string_datatype",
                "units",
                "value_format",
                "value_format_name",
                "alias",
                "convert_tz",
                "suggestable",
                "type",
                "suggest_dimension",
                "suggest_explore"
        ],
        "filter": [
                "case_sensitive",
                "label",
                "required_access_grants",
                "suggestions",
                "view_label",
                "description",
                "group_label",
                "hidden",
                "tags",
                "bypass_suggest_restrictions",
                "datatype",
                "full_suggestions",
                "group_item_label",
                "required_fields",
                "suggest_persist_for",
                "sql",
                "alias",
                "convert_tz",
                "suggestable",
                "type",
                "suggest_dimension",
                "suggest_explore",
                "default_value"
        ],
        "view": [
                "label",
                "dimension",
                "dimension_group",
                "drill_fields",
                "extends",
                "extension",
                "filter",
                "final",
                "measure",
                "parameter",
                "derived_table",
                "required_access_grants",
                "set",
                "sql_table_name",
                "suggestions",
                "view_label"
        ],
        "measure": [
                "label",
                "drill_fields",
                "required_access_grants",
                "view_label",
                "description",
                "group_label",
                "hidden",
                "tags",
                "action",
                "can_filter",
                "datatype",
                "fanout_on",
                "group_item_label",
                "html",
                "label_from_parameter",
                "link",
                "order_by_field",
                "required_fields",
                "sql",
                "value_format",
                "value_format_name",
                "alias",
                "convert_tz",
                "suggestable",
                "type",
                "suggest_dimension",
                "suggest_explore",
                "approximate",
                "approximate_threshold",
                "allow_approximate_optimization",
                "direction",
                "filters",
                "list_field",
                "percentile",
                "precision",
                "sql_distinct_key"
        ],
        "dimension_group": [
                "label",
                "drill_fields",
                "required_access_grants",
                "view_label",
                "description",
                "group_label",
                "hidden",
                "tags",
                "allow_fill",
                "bypass_suggest_restrictions",
                "can_filter",
                "datatype",
                "fanout_on",
                "full_suggestions",
                "group_item_label",
                "html",
                "order_by_field",
                "skip_drill_filter",
                "sql",
                "sql_end",
                "sql_start",
                "alias",
                "convert_tz",
                "suggestable",
                "type",
                "suggest_dimension",
                "suggest_explore",
                "intervals",
                "timeframes"
        ],
        "parameter": [
                "label",
                "required_access_grants",
                "suggestions",
                "view_label",
                "description",
                "group_label",
                "hidden",
                "tags",
                "bypass_suggest_restrictions",
                "full_suggestions",
                "group_item_label",
                "required_fields",
                "suggest_persist_for",
                "alias",
                "convert_tz",
                "suggestable",
                "type",
                "suggest_dimension",
                "suggest_explore",
                "default_value",
                "allowed_value"
        ],
        "query": [
                "label",
                "description",
                "group_label",
                "filters",
                "limit",
                "sorts",
                "timezone",
                "dimensions",
                "measures",
                "pivots"
        ],
        "application": [
                "label",
                "url",
                "file",
                "entitlements"
        ],
        "visualization": [
                "label",
                "url",
                "file",
                "id",
                "sri_hash",
                "dependencies"
        ],
        "action": [
                "label",
                "url",
                "icon_url",
                "form_url",
                "param",
                "form_param",
                "user_attribute_param"
        ],
        "form_param": [
                "label",
                "description",
                "type",
                "name",
                "option",
                "required",
                "default"
        ],
        "option": [
                "label",
                "name"
        ],
        "map_layer": [
                "label",
                "url",
                "file",
                "extents_json_url",
                "feature_key",
                "format",
                "max_zoom_level",
                "min_zoom_level",
                "projection",
                "property_key",
                "property_label_key"
        ],
        "datagroup": [
                "label",
                "description",
                "max_cache_age",
                "sql_trigger"
        ],
        "when": [
                "label",
                "sql"
        ],
        "link": [
                "label",
                "url",
                "icon_url"
        ],
        "allowed_value": [
                "label",
                "value"
        ],
        "derived_table": [
                "persist_for",
                "sql",
                "cluster_keys",
                "create_process",
                "datagroup_trigger",
                "distribution",
                "distribution_style",
                "explore_source",
                "indexes",
                "partition_keys",
                "sortkeys",
                "sql_create",
                "sql_trigger_value",
                "table_compression",
                "table_format",
                "publish_as_db_view"
        ],
        "materialization": [
                "persist_for",
                "datagroup_trigger",
                "sql_trigger_value"
        ],
        "manifest": [
                "local_dependency",
                "remote_dependency",
                "localization_settings",
                "project_name",
                "constant",
                "application",
                "visualization"
        ],
        "join": [
                "required_access_grants",
                "sql_table_name",
                "view_label",
                "from",
                "fields",
                "sql",
                "type",
                "foreign_key",
                "outer_only",
                "relationship",
                "required_joins",
                "sql_foreign_key",
                "sql_on",
                "sql_where"
        ],
        "set": [
                "fields"
        ],
        "derived_column": [
                "sql"
        ],
        "named_value_format": [
                "value_format",
                "strict_value_format"
        ],
        "explore_source": [
                "filters",
                "expression_custom_filter",
                "limit",
                "column",
                "derived_column",
                "bind_all_filters",
                "bind_filters",
                "sorts",
                "timezone"
        ],
        "always_filter": [
                "filters"
        ],
        "test": [
                "explore_source",
                "assert"
        ],
        "aggregate_table": [
                "query",
                "materialization"
        ],
        "remote_dependency": [
                "url",
                "ref",
                "override_constant"
        ],
        "entitlements": [
                "local_storage",
                "navigation",
                "new_window",
                "allow_forms",
                "allow_same_origin",
                "core_api_methods",
                "external_api_urls",
                "oauth2_urls",
                "global_user_attributes",
                "scoped_user_attributes",
                "new_window_external_urls",
                "use_form_submit",
                "use_embeds"
        ],
        "param": [
                "name",
                "value"
        ],
        "user_attribute_param": [
                "name",
                "user_attribute"
        ],
        "case": [
                "when",
                "else"
        ],
        "column": [
                "field"
        ],
        "access_filter": [
                "field",
                "user_attribute"
        ],
        "bind_filters": [
                "from_field",
                "to_field"
        ],
        "access_grant": [
                "allowed_values",
                "user_attribute"
        ],
        "create_process": [
                "sql_step"
        ],
        "override_constant": [
                "value"
        ],
        "constant": [
                "value",
                "export"
        ],
        "local_dependency": [
                "project"
        ],
        "localization_settings": [
                "default_locale",
                "localization_level"
        ]
}