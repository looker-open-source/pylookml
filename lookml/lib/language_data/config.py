config = \
{
        "access_grant": {
                "model": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/access_grant?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "case_sensitive": {
                "model": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 0,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/case_sensitive?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 1,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/case_sensitive?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/case_sensitive?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/case_sensitive?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "connection": {
                "model": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/connection?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "datagroup": {
                "model": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/datagroup?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "explore": {
                "model": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/explore?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "fiscal_month_offset": {
                "model": {
                        "type": "string_unquoted",
                        "subtype": "number",
                        "indent": 0,
                        "default_value": "0",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/fiscal_month_offset?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "include": {
                "model": {
                        "type": "include",
                        "subtype": "string",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/include?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "label": {
                "model": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "view": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "query": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "application": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/application/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "visualization": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/visualization?version=7.18&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "action": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/action/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "form_param": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/form_param/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "option": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 5,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/option/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "map_layer": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "datagroup": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/datagroup/label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "when": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 5,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/case/when?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "link": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/field-params/link?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "allowed_value": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/field-params/parameter?version=7.14&lookml=new#specifying_allowed_values",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "map_layer": {
                "model": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/map_layer?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "named_value_format": {
                "model": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/named_value_format?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "persist_for": {
                "model": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/persist_for?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/persist_for?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "derived_table": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/persist_for?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "materialization": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/materialization/persist_for?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "persist_with": {
                "model": {
                        "type": "string_unquoted",
                        "subtype": "datagroup-ref",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/persist_with?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "string_unquoted",
                        "subtype": "datagroup-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/persist_with?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "test": {
                "model": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/test?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "view": {
                "model": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/view?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "week_start_day": {
                "model": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 0,
                        "default_value": "monday",
                        "docs_url": "https://looker.com/docs/r/lookml/types/model/week_start_day?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "monday",
                                "tuesday",
                                "wednesday",
                                "thursday",
                                "friday",
                                "saturday",
                                "sunday"
                        ]
                }
        },
        "local_dependency": {
                "manifest": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/local_dependency?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "remote_dependency": {
                "manifest": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/remote_dependency?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "localization_settings": {
                "manifest": {
                        "type": "anonymous_construct",
                        "subtype": "anonymous_construct",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/localization_settings?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "project_name": {
                "manifest": {
                        "type": "string",
                        "subtype": "project-name",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/project_name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "constant": {
                "manifest": {
                        "type": "named_construct",
                        "subtype": "constant-ref",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/constant?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "application": {
                "manifest": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 0,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/application?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "dimension": {
                "view": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/dimension?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "dimension_group": {
                "view": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/dimension_group?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "drill_fields": {
                "view": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/drill_fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/drill_fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/drill_fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/drill_fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "extends": {
                "view": {
                        "type": "list_unquoted",
                        "subtype": "view-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/extends?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "list_unquoted",
                        "subtype": "explore-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/extends?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "extension": {
                "view": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 1,
                        "default_value": "required",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/extension?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "required"
                        ]
                },
                "explore": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 1,
                        "default_value": "required",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/extension?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "required"
                        ]
                }
        },
        "filter": {
                "view": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "final": {
                "view": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 1,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/final?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 1,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/final?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "measure": {
                "view": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/measure?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "parameter": {
                "view": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/parameter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "derived_table": {
                "view": {
                        "type": "anonymous_construct",
                        "subtype": "anonymous_construct",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/derived_table?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "required_access_grants": {
                "view": {
                        "type": "list_unquoted",
                        "subtype": "access-grant-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/required_access_grants?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "list_unquoted",
                        "subtype": "access-grant-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/required_access_grants?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "list_unquoted",
                        "subtype": "access-grant-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/required_access_grants?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "list_unquoted",
                        "subtype": "access-grant-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/required_access_grants?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "list_unquoted",
                        "subtype": "access-grant-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/required_access_grants?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "list_unquoted",
                        "subtype": "access-grant-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/required_access_grants?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "list_unquoted",
                        "subtype": "access-grant-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/required_access_grants?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "join": {
                        "type": "list_unquoted",
                        "subtype": "access-grant-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/required_access_grants?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "set": {
                "view": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/set?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_table_name": {
                "view": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/sql_table_name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/sql_table_name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "join": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/sql_table_name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "suggestions": {
                "view": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 1,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/suggestions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/suggestions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/suggestions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/suggestions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "view_label": {
                "view": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/view/view_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/view_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/view_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/view_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/view_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/view_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/view_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "join": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/view_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "access_filter": {
                "explore": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/access_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "aggregate_table": {
                "explore": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/aggregate_table?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "always_filter": {
                "explore": {
                        "type": "anonymous_construct",
                        "subtype": "anonymous_construct",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/always_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "always_join": {
                "explore": {
                        "type": "list_unquoted",
                        "subtype": "view-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/always_join?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "cancel_grouping_fields": {
                "explore": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/cancel_grouping_fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "conditionally_filter": {
                "explore": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/conditionally_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "description": {
                "explore": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/description?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/description?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/description?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/description?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/description?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/description?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "query": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/description?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "form_param": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/form_param/description?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "datagroup": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/datagroup/description?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "group_label": {
                "explore": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/group_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/group_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/group_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/group_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/group_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/group_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "query": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/group_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "from": {
                "explore": {
                        "type": "string_unquoted",
                        "subtype": "view-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/from?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "join": {
                        "type": "string_unquoted",
                        "subtype": "view-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/from?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "fields": {
                "explore": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "join": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "set": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/set/fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "hidden": {
                "explore": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 1,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/hidden?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/hidden?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/hidden?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/hidden?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/hidden?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/hidden?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "join": {
                "explore": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/join?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_always_where": {
                "explore": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/sql_always_where?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_always_having": {
                "explore": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/sql_always_having?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "tags": {
                "explore": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 1,
                        "default_value": [],
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/tags?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 2,
                        "default_value": [],
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/tags?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 2,
                        "default_value": [],
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/tags?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 2,
                        "default_value": [],
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/tags?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 2,
                        "default_value": [],
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/tags?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 2,
                        "default_value": [],
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/tags?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "view_name": {
                "explore": {
                        "type": "string_unquoted",
                        "subtype": "view-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore/view_name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "action": {
                "dimension": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/action?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/action?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "allow_fill": {
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/allow_fill?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/allow_fill?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "alpha_sort": {
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/alpha_sort?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "bypass_suggest_restrictions": {
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/bypass_suggest_restrictions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/bypass_suggest_restrictions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/bypass_suggest_restrictions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/bypass_suggest_restrictions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "can_filter": {
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/can_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/can_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/can_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "case": {
                "dimension": {
                        "type": "anonymous_construct",
                        "subtype": "anonymous_construct",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/case?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "datatype": {
                "dimension": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "timestamp",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/datatype?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "timestamp",
                                "epoch",
                                "date",
                                "datetime",
                                "timestamp",
                                "yyyymmdd"
                        ]
                },
                "measure": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "timestamp",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/datatype?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "timestamp",
                                "epoch",
                                "date",
                                "datetime",
                                "timestamp",
                                "yyyymmdd"
                        ]
                },
                "dimension_group": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "timestamp",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/datatype?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "timestamp",
                                "epoch",
                                "date",
                                "datetime",
                                "timestamp",
                                "yyyymmdd"
                        ]
                },
                "filter": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "timestamp",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/datatype?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "timestamp",
                                "epoch",
                                "date",
                                "datetime",
                                "timestamp",
                                "yyyymmdd"
                        ]
                }
        },
        "end_location_field": {
                "dimension": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/end_location_field?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "fanout_on": {
                "dimension": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/fanout_on?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/fanout_on?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/fanout_on?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "full_suggestions": {
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/full_suggestions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/full_suggestions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/full_suggestions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/full_suggestions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "group_item_label": {
                "dimension": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/group_item_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/group_item_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/group_item_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/group_item_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "string",
                        "subtype": "possibly-localized-string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/group_item_label?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "html": {
                "dimension": {
                        "type": "html",
                        "subtype": "html-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/html?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "html",
                        "subtype": "html-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/html?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "html",
                        "subtype": "html-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/html?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "label_from_parameter": {
                "dimension": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/label_from_parameter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/label_from_parameter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "link": {
                "dimension": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/link?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/link?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "map_layer_name": {
                "dimension": {
                        "type": "string_unquoted",
                        "subtype": "map-layer-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/map_layer_name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "order_by_field": {
                "dimension": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/order_by_field?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/order_by_field?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/order_by_field?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "primary_key": {
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/primary_key?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "required_fields": {
                "dimension": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/required_fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/required_fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/required_fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/required_fields?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "skip_drill_filter": {
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/skip_drill_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/skip_drill_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "start_location_field": {
                "dimension": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/start_location_field?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "suggest_persist_for": {
                "dimension": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/suggest_persist_for?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/suggest_persist_for?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/suggest_persist_for?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "style": {
                "dimension": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "classic",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/style?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "classic",
                                "interval",
                                "integer",
                                "relational"
                        ]
                }
        },
        "sql": {
                "dimension": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/sql?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/sql?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/sql?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/sql?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "derived_table": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/sql?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "join": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/sql?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "derived_column": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 5,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_column/sql?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "when": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 5,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/case/when?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_end": {
                "dimension": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/sql_end?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/sql_end?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_start": {
                "dimension": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/sql_start?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/sql_start?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "tiers": {
                "dimension": {
                        "type": "list_unquoted",
                        "subtype": "number",
                        "indent": 2,
                        "default_value": [],
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/tiers?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_longitude": {
                "dimension": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/sql_longitude?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_latitude": {
                "dimension": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/sql_latitude?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "string_datatype": {
                "dimension": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "unicode",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/string_datatype?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "unicode"
                        ]
                }
        },
        "units": {
                "dimension": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "kilometers",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/units?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "feet",
                                "kilometers",
                                "meters",
                                "miles",
                                "nautical_miles",
                                "yards"
                        ]
                }
        },
        "value_format": {
                "dimension": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/value_format?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/value_format?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "named_value_format": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/named_value_format/value_format?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "value_format_name": {
                "dimension": {
                        "type": "string_unquoted",
                        "subtype": "value-format-ref",
                        "indent": 2,
                        "default_value": "decimal_0",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/value_format_name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string_unquoted",
                        "subtype": "value-format-ref",
                        "indent": 2,
                        "default_value": "decimal_0",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/value_format_name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "alias": {
                "dimension": {
                        "type": "list_unquoted",
                        "subtype": "identifier",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/alias?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "list_unquoted",
                        "subtype": "identifier",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/alias?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "list_unquoted",
                        "subtype": "identifier",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/alias?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "list_unquoted",
                        "subtype": "identifier",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/alias?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "list_unquoted",
                        "subtype": "identifier",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/alias?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "convert_tz": {
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/convert_tz?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/convert_tz?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/convert_tz?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/convert_tz?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/convert_tz?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "suggestable": {
                "dimension": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/suggestable?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/suggestable?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/suggestable?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/suggestable?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "yes",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/suggestable?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "type": {
                "dimension": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "string",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/type?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "date",
                                "distance",
                                "location",
                                "number",
                                "string",
                                "tier",
                                "yesno",
                                "zipcode",
                                "date_day_of_month",
                                "date_day_of_week",
                                "date_day_of_week_index",
                                "date_day_of_year",
                                "date_fiscal_month_num",
                                "date_fiscal_quarter",
                                "date_fiscal_quarter_of_year",
                                "date_fiscal_year",
                                "date_hour",
                                "date_hour2",
                                "date_hour3",
                                "date_hour4",
                                "date_hour6",
                                "date_hour8",
                                "date_hour12",
                                "date_hour_of_day",
                                "date_microsecond",
                                "date_millisecond",
                                "date_millisecond2",
                                "date_millisecond4",
                                "date_millisecond5",
                                "date_millisecond8",
                                "date_millisecond10",
                                "date_millisecond20",
                                "date_millisecond25",
                                "date_millisecond40",
                                "date_millisecond50",
                                "date_millisecond100",
                                "date_millisecond125",
                                "date_millisecond200",
                                "date_millisecond250",
                                "date_millisecond500",
                                "date_minute",
                                "date_minute2",
                                "date_minute3",
                                "date_minute4",
                                "date_minute5",
                                "date_minute6",
                                "date_minute10",
                                "date_minute12",
                                "date_minute15",
                                "date_minute20",
                                "date_minute30",
                                "date_month",
                                "date_month_name",
                                "date_month_num",
                                "date_quarter",
                                "date_quarter_of_year",
                                "date_raw",
                                "date_second",
                                "date_time",
                                "date_time_of_day",
                                "date_week",
                                "date_week_of_year",
                                "date_year",
                                "duration_day",
                                "duration_hour",
                                "duration_minute",
                                "duration_month",
                                "duration_quarter",
                                "duration_second",
                                "duration_week",
                                "duration_year"
                        ]
                },
                "measure": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "number",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/type?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "average",
                                "average_distinct",
                                "count",
                                "count_distinct",
                                "date",
                                "int",
                                "list",
                                "max",
                                "median",
                                "median_distinct",
                                "min",
                                "number",
                                "percent_of_previous",
                                "percent_of_total",
                                "percentile",
                                "percentile_distinct",
                                "running_total",
                                "string",
                                "sum",
                                "sum_distinct",
                                "yesno",
                                "zipcode",
                                "date_date",
                                "date_day_of_month",
                                "date_day_of_week",
                                "date_day_of_week_index",
                                "date_day_of_year",
                                "date_fiscal_month_num",
                                "date_fiscal_quarter",
                                "date_fiscal_quarter_of_year",
                                "date_fiscal_year",
                                "date_hour",
                                "date_hour2",
                                "date_hour3",
                                "date_hour4",
                                "date_hour6",
                                "date_hour8",
                                "date_hour12",
                                "date_hour_of_day",
                                "date_microsecond",
                                "date_millisecond",
                                "date_millisecond2",
                                "date_millisecond4",
                                "date_millisecond5",
                                "date_millisecond8",
                                "date_millisecond10",
                                "date_millisecond20",
                                "date_millisecond25",
                                "date_millisecond40",
                                "date_millisecond50",
                                "date_millisecond100",
                                "date_millisecond125",
                                "date_millisecond200",
                                "date_millisecond250",
                                "date_millisecond500",
                                "date_minute",
                                "date_minute2",
                                "date_minute3",
                                "date_minute4",
                                "date_minute5",
                                "date_minute6",
                                "date_minute10",
                                "date_minute12",
                                "date_minute15",
                                "date_minute20",
                                "date_minute30",
                                "date_month",
                                "date_month_name",
                                "date_month_num",
                                "date_quarter",
                                "date_quarter_of_year",
                                "date_raw",
                                "date_second",
                                "date_time",
                                "date_time_of_day",
                                "date_week",
                                "date_week_of_year",
                                "date_year"
                        ]
                },
                "dimension_group": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "time",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/type?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "duration",
                                "time"
                        ]
                },
                "filter": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "string",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/type?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "date",
                                "distance",
                                "location",
                                "number",
                                "string",
                                "tier",
                                "yesno",
                                "zipcode",
                                "date_day_of_month",
                                "date_day_of_week",
                                "date_day_of_week_index",
                                "date_day_of_year",
                                "date_fiscal_month_num",
                                "date_fiscal_quarter",
                                "date_fiscal_quarter_of_year",
                                "date_fiscal_year",
                                "date_hour",
                                "date_hour2",
                                "date_hour3",
                                "date_hour4",
                                "date_hour6",
                                "date_hour8",
                                "date_hour12",
                                "date_hour_of_day",
                                "date_microsecond",
                                "date_millisecond",
                                "date_millisecond2",
                                "date_millisecond4",
                                "date_millisecond5",
                                "date_millisecond8",
                                "date_millisecond10",
                                "date_millisecond20",
                                "date_millisecond25",
                                "date_millisecond40",
                                "date_millisecond50",
                                "date_millisecond100",
                                "date_millisecond125",
                                "date_millisecond200",
                                "date_millisecond250",
                                "date_millisecond500",
                                "date_minute",
                                "date_minute2",
                                "date_minute3",
                                "date_minute4",
                                "date_minute5",
                                "date_minute6",
                                "date_minute10",
                                "date_minute12",
                                "date_minute15",
                                "date_minute20",
                                "date_minute30",
                                "date_month",
                                "date_month_name",
                                "date_month_num",
                                "date_quarter",
                                "date_quarter_of_year",
                                "date_raw",
                                "date_second",
                                "date_time",
                                "date_time_of_day",
                                "date_week",
                                "date_week_of_year",
                                "date_year",
                                "duration_day",
                                "duration_hour",
                                "duration_minute",
                                "duration_month",
                                "duration_quarter",
                                "duration_second",
                                "duration_week",
                                "duration_year"
                        ]
                },
                "parameter": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 2,
                        "default_value": "string",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/type?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "date",
                                "date_time",
                                "number",
                                "string",
                                "unquoted",
                                "yesno"
                        ]
                },
                "join": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 3,
                        "default_value": "left_outer",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/type?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "cross",
                                "full_outer",
                                "inner",
                                "left_outer"
                        ]
                },
                "form_param": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 4,
                        "default_value": "textarea",
                        "docs_url": "https://looker.com/docs/r/lookml/types/form_param/type?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "select",
                                "string",
                                "textarea"
                        ]
                }
        },
        "suggest_dimension": {
                "dimension": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/suggest_dimension?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/suggest_dimension?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/suggest_dimension?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/suggest_dimension?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/suggest_dimension?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "suggest_explore": {
                "dimension": {
                        "type": "string_unquoted",
                        "subtype": "explore-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension/suggest_explore?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "measure": {
                        "type": "string_unquoted",
                        "subtype": "explore-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/suggest_explore?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "dimension_group": {
                        "type": "string_unquoted",
                        "subtype": "explore-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/suggest_explore?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "filter": {
                        "type": "string_unquoted",
                        "subtype": "explore-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/suggest_explore?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "string_unquoted",
                        "subtype": "explore-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/suggest_explore?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "approximate": {
                "measure": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/approximate?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "approximate_threshold": {
                "measure": {
                        "type": "string_unquoted",
                        "subtype": "number",
                        "indent": 2,
                        "default_value": "100000",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/approximate_threshold?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "allow_approximate_optimization": {
                "measure": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 2,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/allow_approximate_optimization?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "direction": {
                "measure": {
                        "type": "options_quoted",
                        "subtype": "options_quoted",
                        "indent": 2,
                        "default_value": "row",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/direction?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "row",
                                "column"
                        ]
                }
        },
        "filters": {
                "measure": {
                        "type": "filters",
                        "subtype": "identifier",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/filters?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore_source": {
                        "type": "filters",
                        "subtype": "identifier",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore_source/filters?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "query": {
                        "type": "filters",
                        "subtype": "identifier",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/filters?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "always_filter": {
                        "type": "filters",
                        "subtype": "identifier",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/explore-params/always_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "list_field": {
                "measure": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/list_field?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "percentile": {
                "measure": {
                        "type": "string_unquoted",
                        "subtype": "number",
                        "indent": 2,
                        "default_value": "75",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/percentile?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "precision": {
                "measure": {
                        "type": "string_unquoted",
                        "subtype": "number",
                        "indent": 2,
                        "default_value": "6",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/precision?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_distinct_key": {
                "measure": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/measure/sql_distinct_key?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "intervals": {
                "dimension_group": {
                        "type": "list_unquoted",
                        "subtype": "list_unquoted",
                        "indent": 2,
                        "default_value": "day",
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/intervals?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "day",
                                "hour",
                                "minute",
                                "month",
                                "quarter",
                                "second",
                                "week",
                                "year"
                        ]
                }
        },
        "timeframes": {
                "dimension_group": {
                        "type": "list_unquoted",
                        "subtype": "list_unquoted",
                        "indent": 2,
                        "default_value": [
                                "date",
                                "month",
                                "raw"
                        ],
                        "docs_url": "https://looker.com/docs/r/lookml/types/dimension_group/timeframes?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "date",
                                "day_of_month",
                                "day_of_week",
                                "day_of_week_index",
                                "day_of_year",
                                "fiscal_month_num",
                                "fiscal_quarter",
                                "fiscal_quarter_of_year",
                                "fiscal_year",
                                "hour",
                                "hour2",
                                "hour3",
                                "hour4",
                                "hour6",
                                "hour8",
                                "hour12",
                                "hour_of_day",
                                "microsecond",
                                "millisecond",
                                "millisecond2",
                                "millisecond4",
                                "millisecond5",
                                "millisecond8",
                                "millisecond10",
                                "millisecond20",
                                "millisecond25",
                                "millisecond40",
                                "millisecond50",
                                "millisecond100",
                                "millisecond125",
                                "millisecond200",
                                "millisecond250",
                                "millisecond500",
                                "minute",
                                "minute2",
                                "minute3",
                                "minute4",
                                "minute5",
                                "minute6",
                                "minute10",
                                "minute12",
                                "minute15",
                                "minute20",
                                "minute30",
                                "month",
                                "month_name",
                                "month_num",
                                "quarter",
                                "quarter_of_year",
                                "raw",
                                "second",
                                "time",
                                "time_of_day",
                                "week",
                                "week_of_year",
                                "year",
                                "yesno"
                        ]
                }
        },
        "default_value": {
                "filter": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/filter/default_value?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "parameter": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/default_value?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "allowed_value": {
                "parameter": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/parameter/allowed_value?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "cluster_keys": {
                "derived_table": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/cluster_keys?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "create_process": {
                "derived_table": {
                        "type": "anonymous_construct",
                        "subtype": "anonymous_construct",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/create_process?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "datagroup_trigger": {
                "derived_table": {
                        "type": "string_unquoted",
                        "subtype": "datagroup-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/datagroup_trigger?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "materialization": {
                        "type": "string_unquoted",
                        "subtype": "datagroup-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/materialization/datagroup_trigger?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "distribution": {
                "derived_table": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/distribution?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "distribution_style": {
                "derived_table": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 3,
                        "default_value": "even",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/distribution_style?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "all",
                                "even"
                        ]
                }
        },
        "explore_source": {
                "derived_table": {
                        "type": "named_construct_single",
                        "subtype": "explore-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/explore_source?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "test": {
                        "type": "string_unquoted",
                        "subtype": "explore-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/test/explore_source?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "indexes": {
                "derived_table": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/indexes?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "partition_keys": {
                "derived_table": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/partition_keys?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sortkeys": {
                "derived_table": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/sortkeys?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_create": {
                "derived_table": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/sql_create?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_trigger_value": {
                "derived_table": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/sql_trigger_value?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "materialization": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/materialization/sql_trigger_value?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "table_compression": {
                "derived_table": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 3,
                        "default_value": "GZIP",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/table_compression?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "GZIP",
                                "SNAPPY"
                        ]
                }
        },
        "table_format": {
                "derived_table": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 3,
                        "default_value": "PARQUET",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/table_format?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "PARQUET",
                                "ORC",
                                "AVRO",
                                "JSON",
                                "TEXTFILE"
                        ]
                }
        },
        "publish_as_db_view": {
                "derived_table": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 3,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/derived_table/publish_as_db_view?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "expression_custom_filter": {
                "explore_source": {
                        "type": "expression",
                        "subtype": "expression-block",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore_source/expression_custom_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "limit": {
                "explore_source": {
                        "type": "string_unquoted",
                        "subtype": "number",
                        "indent": 4,
                        "default_value": "5000",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore_source/limit?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "query": {
                        "type": "string_unquoted",
                        "subtype": "number",
                        "indent": 3,
                        "default_value": "5000",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/limit?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "column": {
                "explore_source": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore_source/column?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "derived_column": {
                "explore_source": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore_source/derived_column?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "bind_all_filters": {
                "explore_source": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 4,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore_source/bind_all_filters?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "bind_filters": {
                "explore_source": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore_source/bind_filters?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sorts": {
                "explore_source": {
                        "type": "sorts",
                        "subtype": "field-ref-to-sort-map",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore_source/sorts?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "query": {
                        "type": "sorts",
                        "subtype": "field-ref-to-sort-map",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/sorts?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "timezone": {
                "explore_source": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 4,
                        "default_value": "America/Los_Angeles",
                        "docs_url": "https://looker.com/docs/r/lookml/types/explore_source/timezone?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "Africa/Abidjan",
                                "Africa/Accra",
                                "Africa/Addis_Ababa",
                                "Africa/Algiers",
                                "Africa/Asmara",
                                "Africa/Bamako",
                                "Africa/Bangui",
                                "Africa/Banjul",
                                "Africa/Bissau",
                                "Africa/Blantyre",
                                "Africa/Brazzaville",
                                "Africa/Bujumbura",
                                "Africa/Cairo",
                                "Africa/Casablanca",
                                "Africa/Ceuta",
                                "Africa/Conakry",
                                "Africa/Dakar",
                                "Africa/Dar_es_Salaam",
                                "Africa/Djibouti",
                                "Africa/Douala",
                                "Africa/El_Aaiun",
                                "Africa/Freetown",
                                "Africa/Gaborone",
                                "Africa/Harare",
                                "Africa/Johannesburg",
                                "Africa/Juba",
                                "Africa/Kampala",
                                "Africa/Khartoum",
                                "Africa/Kigali",
                                "Africa/Kinshasa",
                                "Africa/Lagos",
                                "Africa/Libreville",
                                "Africa/Lome",
                                "Africa/Luanda",
                                "Africa/Lubumbashi",
                                "Africa/Lusaka",
                                "Africa/Malabo",
                                "Africa/Maputo",
                                "Africa/Maseru",
                                "Africa/Mbabane",
                                "Africa/Mogadishu",
                                "Africa/Monrovia",
                                "Africa/Nairobi",
                                "Africa/Ndjamena",
                                "Africa/Niamey",
                                "Africa/Nouakchott",
                                "Africa/Ouagadougou",
                                "Africa/Porto-Novo",
                                "Africa/Sao_Tome",
                                "Africa/Timbuktu",
                                "Africa/Tripoli",
                                "Africa/Tunis",
                                "Africa/Windhoek",
                                "America/Adak",
                                "America/Anchorage",
                                "America/Anguilla",
                                "America/Antigua",
                                "America/Araguaina",
                                "America/Argentina/Buenos_Aires",
                                "America/Argentina/Catamarca",
                                "America/Argentina/ComodRivadavia",
                                "America/Argentina/Cordoba",
                                "America/Argentina/Jujuy",
                                "America/Argentina/La_Rioja",
                                "America/Argentina/Mendoza",
                                "America/Argentina/Rio_Gallegos",
                                "America/Argentina/Salta",
                                "America/Argentina/San_Juan",
                                "America/Argentina/San_Luis",
                                "America/Argentina/Tucuman",
                                "America/Argentina/Ushuaia",
                                "America/Aruba",
                                "America/Asuncion",
                                "America/Atikokan",
                                "America/Atka",
                                "America/Bahia",
                                "America/Bahia_Banderas",
                                "America/Barbados",
                                "America/Belem",
                                "America/Belize",
                                "America/Blanc-Sablon",
                                "America/Boa_Vista",
                                "America/Bogota",
                                "America/Boise",
                                "America/Buenos_Aires",
                                "America/Cambridge_Bay",
                                "America/Campo_Grande",
                                "America/Cancun",
                                "America/Caracas",
                                "America/Catamarca",
                                "America/Cayenne",
                                "America/Cayman",
                                "America/Chicago",
                                "America/Chihuahua",
                                "America/Coral_Harbour",
                                "America/Cordoba",
                                "America/Costa_Rica",
                                "America/Creston",
                                "America/Cuiaba",
                                "America/Curacao",
                                "America/Danmarkshavn",
                                "America/Dawson",
                                "America/Dawson_Creek",
                                "America/Denver",
                                "America/Detroit",
                                "America/Dominica",
                                "America/Edmonton",
                                "America/Eirunepe",
                                "America/El_Salvador",
                                "America/Ensenada",
                                "America/Fort_Nelson",
                                "America/Fort_Wayne",
                                "America/Fortaleza",
                                "America/Glace_Bay",
                                "America/Godthab",
                                "America/Goose_Bay",
                                "America/Grand_Turk",
                                "America/Grenada",
                                "America/Guadeloupe",
                                "America/Guatemala",
                                "America/Guayaquil",
                                "America/Guyana",
                                "America/Halifax",
                                "America/Havana",
                                "America/Hermosillo",
                                "America/Indiana/Indianapolis",
                                "America/Indiana/Knox",
                                "America/Indiana/Marengo",
                                "America/Indiana/Petersburg",
                                "America/Indiana/Tell_City",
                                "America/Indiana/Vevay",
                                "America/Indiana/Vincennes",
                                "America/Indiana/Winamac",
                                "America/Indianapolis",
                                "America/Inuvik",
                                "America/Iqaluit",
                                "America/Jamaica",
                                "America/Jujuy",
                                "America/Juneau",
                                "America/Kentucky/Louisville",
                                "America/Kentucky/Monticello",
                                "America/Knox_IN",
                                "America/Kralendijk",
                                "America/La_Paz",
                                "America/Lima",
                                "America/Los_Angeles",
                                "America/Louisville",
                                "America/Lower_Princes",
                                "America/Maceio",
                                "America/Managua",
                                "America/Manaus",
                                "America/Marigot",
                                "America/Martinique",
                                "America/Matamoros",
                                "America/Mazatlan",
                                "America/Mendoza",
                                "America/Menominee",
                                "America/Merida",
                                "America/Metlakatla",
                                "America/Mexico_City",
                                "America/Miquelon",
                                "America/Moncton",
                                "America/Monterrey",
                                "America/Montevideo",
                                "America/Montreal",
                                "America/Montserrat",
                                "America/Nassau",
                                "America/New_York",
                                "America/Nipigon",
                                "America/Nome",
                                "America/Noronha",
                                "America/North_Dakota/Beulah",
                                "America/North_Dakota/Center",
                                "America/North_Dakota/New_Salem",
                                "America/Ojinaga",
                                "America/Panama",
                                "America/Pangnirtung",
                                "America/Paramaribo",
                                "America/Phoenix",
                                "America/Port_of_Spain",
                                "America/Port-au-Prince",
                                "America/Porto_Acre",
                                "America/Porto_Velho",
                                "America/Puerto_Rico",
                                "America/Punta_Arenas",
                                "America/Rainy_River",
                                "America/Rankin_Inlet",
                                "America/Recife",
                                "America/Regina",
                                "America/Resolute",
                                "America/Rio_Branco",
                                "America/Rosario",
                                "America/Santa_Isabel",
                                "America/Santarem",
                                "America/Santiago",
                                "America/Santo_Domingo",
                                "America/Sao_Paulo",
                                "America/Scoresbysund",
                                "America/Shiprock",
                                "America/Sitka",
                                "America/St_Barthelemy",
                                "America/St_Johns",
                                "America/St_Kitts",
                                "America/St_Lucia",
                                "America/St_Thomas",
                                "America/St_Vincent",
                                "America/Swift_Current",
                                "America/Tegucigalpa",
                                "America/Thule",
                                "America/Thunder_Bay",
                                "America/Tijuana",
                                "America/Toronto",
                                "America/Tortola",
                                "America/Vancouver",
                                "America/Virgin",
                                "America/Whitehorse",
                                "America/Winnipeg",
                                "America/Yakutat",
                                "America/Yellowknife",
                                "Antarctica/Casey",
                                "Antarctica/Davis",
                                "Antarctica/DumontDUrville",
                                "Antarctica/Macquarie",
                                "Antarctica/Mawson",
                                "Antarctica/McMurdo",
                                "Antarctica/Palmer",
                                "Antarctica/Rothera",
                                "Antarctica/South_Pole",
                                "Antarctica/Syowa",
                                "Antarctica/Troll",
                                "Antarctica/Vostok",
                                "Arctic/Longyearbyen",
                                "Asia/Aden",
                                "Asia/Almaty",
                                "Asia/Amman",
                                "Asia/Anadyr",
                                "Asia/Aqtau",
                                "Asia/Aqtobe",
                                "Asia/Ashgabat",
                                "Asia/Ashkhabad",
                                "Asia/Atyrau",
                                "Asia/Baghdad",
                                "Asia/Bahrain",
                                "Asia/Baku",
                                "Asia/Bangkok",
                                "Asia/Barnaul",
                                "Asia/Beirut",
                                "Asia/Bishkek",
                                "Asia/Brunei",
                                "Asia/Calcutta",
                                "Asia/Chita",
                                "Asia/Choibalsan",
                                "Asia/Chongqing",
                                "Asia/Chungking",
                                "Asia/Colombo",
                                "Asia/Dacca",
                                "Asia/Damascus",
                                "Asia/Dhaka",
                                "Asia/Dili",
                                "Asia/Dubai",
                                "Asia/Dushanbe",
                                "Asia/Famagusta",
                                "Asia/Gaza",
                                "Asia/Harbin",
                                "Asia/Hebron",
                                "Asia/Ho_Chi_Minh",
                                "Asia/Hong_Kong",
                                "Asia/Hovd",
                                "Asia/Irkutsk",
                                "Asia/Istanbul",
                                "Asia/Jakarta",
                                "Asia/Jayapura",
                                "Asia/Jerusalem",
                                "Asia/Kabul",
                                "Asia/Kamchatka",
                                "Asia/Karachi",
                                "Asia/Kashgar",
                                "Asia/Kathmandu",
                                "Asia/Katmandu",
                                "Asia/Khandyga",
                                "Asia/Kolkata",
                                "Asia/Krasnoyarsk",
                                "Asia/Kuala_Lumpur",
                                "Asia/Kuching",
                                "Asia/Kuwait",
                                "Asia/Macao",
                                "Asia/Macau",
                                "Asia/Magadan",
                                "Asia/Makassar",
                                "Asia/Manila",
                                "Asia/Muscat",
                                "Asia/Novokuznetsk",
                                "Asia/Novosibirsk",
                                "Asia/Omsk",
                                "Asia/Oral",
                                "Asia/Phnom_Penh",
                                "Asia/Pontianak",
                                "Asia/Pyongyang",
                                "Asia/Qatar",
                                "Asia/Qyzylorda",
                                "Asia/Rangoon",
                                "Asia/Riyadh",
                                "Asia/Saigon",
                                "Asia/Sakhalin",
                                "Asia/Samarkand",
                                "Asia/Seoul",
                                "Asia/Shanghai",
                                "Asia/Singapore",
                                "Asia/Srednekolymsk",
                                "Asia/Taipei",
                                "Asia/Tashkent",
                                "Asia/Tbilisi",
                                "Asia/Tehran",
                                "Asia/Tel_Aviv",
                                "Asia/Thimbu",
                                "Asia/Thimphu",
                                "Asia/Tokyo",
                                "Asia/Tomsk",
                                "Asia/Ujung_Pandang",
                                "Asia/Ulaanbaatar",
                                "Asia/Ulan_Bator",
                                "Asia/Urumqi",
                                "Asia/Ust-Nera",
                                "Asia/Vientiane",
                                "Asia/Vladivostok",
                                "Asia/Yakutsk",
                                "Asia/Yangon",
                                "Asia/Yekaterinburg",
                                "Asia/Yerevan",
                                "Atlantic/Azores",
                                "Atlantic/Bermuda",
                                "Atlantic/Canary",
                                "Atlantic/Cape_Verde",
                                "Atlantic/Faeroe",
                                "Atlantic/Faroe",
                                "Atlantic/Jan_Mayen",
                                "Atlantic/Madeira",
                                "Atlantic/Reykjavik",
                                "Atlantic/South_Georgia",
                                "Atlantic/St_Helena",
                                "Atlantic/Stanley",
                                "Australia/ACT",
                                "Australia/Adelaide",
                                "Australia/Brisbane",
                                "Australia/Broken_Hill",
                                "Australia/Canberra",
                                "Australia/Currie",
                                "Australia/Darwin",
                                "Australia/Eucla",
                                "Australia/Hobart",
                                "Australia/LHI",
                                "Australia/Lindeman",
                                "Australia/Lord_Howe",
                                "Australia/Melbourne",
                                "Australia/North",
                                "Australia/NSW",
                                "Australia/Perth",
                                "Australia/Queensland",
                                "Australia/South",
                                "Australia/Sydney",
                                "Australia/Tasmania",
                                "Australia/Victoria",
                                "Australia/West",
                                "Australia/Yancowinna",
                                "Brazil/Acre",
                                "Brazil/DeNoronha",
                                "Brazil/East",
                                "Brazil/West",
                                "Canada/Atlantic",
                                "Canada/Central",
                                "Canada/Eastern",
                                "Canada/Mountain",
                                "Canada/Newfoundland",
                                "Canada/Pacific",
                                "Canada/Saskatchewan",
                                "Canada/Yukon",
                                "CET",
                                "Chile/Continental",
                                "Chile/EasterIsland",
                                "CST6CDT",
                                "Cuba",
                                "EET",
                                "Egypt",
                                "Eire",
                                "EST",
                                "EST5EDT",
                                "Etc/GMT",
                                "Etc/GMT+0",
                                "Etc/GMT+1",
                                "Etc/GMT+10",
                                "Etc/GMT+11",
                                "Etc/GMT+12",
                                "Etc/GMT+2",
                                "Etc/GMT+3",
                                "Etc/GMT+4",
                                "Etc/GMT+5",
                                "Etc/GMT+6",
                                "Etc/GMT+7",
                                "Etc/GMT+8",
                                "Etc/GMT+9",
                                "Etc/GMT0",
                                "Etc/GMT-0",
                                "Etc/GMT-1",
                                "Etc/GMT-10",
                                "Etc/GMT-11",
                                "Etc/GMT-12",
                                "Etc/GMT-13",
                                "Etc/GMT-14",
                                "Etc/GMT-2",
                                "Etc/GMT-3",
                                "Etc/GMT-4",
                                "Etc/GMT-5",
                                "Etc/GMT-6",
                                "Etc/GMT-7",
                                "Etc/GMT-8",
                                "Etc/GMT-9",
                                "Etc/Greenwich",
                                "Etc/UCT",
                                "Etc/Universal",
                                "Etc/UTC",
                                "Etc/Zulu",
                                "Europe/Amsterdam",
                                "Europe/Andorra",
                                "Europe/Astrakhan",
                                "Europe/Athens",
                                "Europe/Belfast",
                                "Europe/Belgrade",
                                "Europe/Sarajevo",
                                "Europe/Berlin",
                                "Europe/Bratislava",
                                "Europe/Brussels",
                                "Europe/Bucharest",
                                "Europe/Budapest",
                                "Europe/Busingen",
                                "Europe/Chisinau",
                                "Europe/Copenhagen",
                                "Europe/Dublin",
                                "Europe/Gibraltar",
                                "Europe/Guernsey",
                                "Europe/Helsinki",
                                "Europe/Isle_of_Man",
                                "Europe/Istanbul",
                                "Europe/Jersey",
                                "Europe/Kaliningrad",
                                "Europe/Kiev",
                                "Europe/Kirov",
                                "Europe/Lisbon",
                                "Europe/Ljubljana",
                                "Europe/London",
                                "Europe/Luxembourg",
                                "Europe/Madrid",
                                "Europe/Malta",
                                "Europe/Mariehamn",
                                "Europe/Minsk",
                                "Europe/Monaco",
                                "Europe/Moscow",
                                "Asia/Nicosia",
                                "Europe/Oslo",
                                "Europe/Paris",
                                "Europe/Podgorica",
                                "Europe/Prague",
                                "Europe/Riga",
                                "Europe/Rome",
                                "Europe/Samara",
                                "Europe/San_Marino",
                                "Europe/Sarajevo",
                                "Europe/Saratov",
                                "Europe/Simferopol",
                                "Europe/Skopje",
                                "Europe/Sofia",
                                "Europe/Stockholm",
                                "Europe/Tallinn",
                                "Europe/Tirane",
                                "Europe/Tiraspol",
                                "Europe/Ulyanovsk",
                                "Europe/Uzhgorod",
                                "Europe/Vaduz",
                                "Europe/Vatican",
                                "Europe/Vienna",
                                "Europe/Vilnius",
                                "Europe/Volgograd",
                                "Europe/Warsaw",
                                "Europe/Zagreb",
                                "Europe/Zaporozhye",
                                "Europe/Zurich",
                                "GB",
                                "GB-Eire",
                                "GMT",
                                "GMT+0",
                                "GMT0",
                                "GMT-0",
                                "Greenwich",
                                "Hongkong",
                                "HST",
                                "Iceland",
                                "Indian/Antananarivo",
                                "Indian/Chagos",
                                "Indian/Christmas",
                                "Indian/Cocos",
                                "Indian/Comoro",
                                "Indian/Kerguelen",
                                "Indian/Mahe",
                                "Indian/Maldives",
                                "Indian/Mauritius",
                                "Indian/Mayotte",
                                "Indian/Reunion",
                                "Iran",
                                "Israel",
                                "Jamaica",
                                "Japan",
                                "Kwajalein",
                                "Libya",
                                "MET",
                                "Mexico/BajaNorte",
                                "Mexico/BajaSur",
                                "Mexico/General",
                                "MST",
                                "MST7MDT",
                                "Navajo",
                                "NZ",
                                "NZ-CHAT",
                                "Pacific/Apia",
                                "Pacific/Auckland",
                                "Pacific/Bougainville",
                                "Pacific/Chatham",
                                "Pacific/Chuuk",
                                "Pacific/Easter",
                                "Pacific/Efate",
                                "Pacific/Enderbury",
                                "Pacific/Fakaofo",
                                "Pacific/Fiji",
                                "Pacific/Funafuti",
                                "Pacific/Galapagos",
                                "Pacific/Gambier",
                                "Pacific/Guadalcanal",
                                "Pacific/Guam",
                                "Pacific/Honolulu",
                                "Pacific/Johnston",
                                "Pacific/Kiritimati",
                                "Pacific/Kosrae",
                                "Pacific/Kwajalein",
                                "Pacific/Majuro",
                                "Pacific/Marquesas",
                                "Pacific/Midway",
                                "Pacific/Nauru",
                                "Pacific/Niue",
                                "Pacific/Norfolk",
                                "Pacific/Noumea",
                                "Pacific/Pago_Pago",
                                "Pacific/Palau",
                                "Pacific/Pitcairn",
                                "Pacific/Pohnpei",
                                "Pacific/Ponape",
                                "Pacific/Port_Moresby",
                                "Pacific/Rarotonga",
                                "Pacific/Saipan",
                                "Pacific/Samoa",
                                "Pacific/Tahiti",
                                "Pacific/Tarawa",
                                "Pacific/Tongatapu",
                                "Pacific/Truk",
                                "Pacific/Wake",
                                "Pacific/Wallis"
                        ]
                },
                "query": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 3,
                        "default_value": "America/Los_Angeles",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/timezone?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "Africa/Abidjan",
                                "Africa/Accra",
                                "Africa/Addis_Ababa",
                                "Africa/Algiers",
                                "Africa/Asmara",
                                "Africa/Bamako",
                                "Africa/Bangui",
                                "Africa/Banjul",
                                "Africa/Bissau",
                                "Africa/Blantyre",
                                "Africa/Brazzaville",
                                "Africa/Bujumbura",
                                "Africa/Cairo",
                                "Africa/Casablanca",
                                "Africa/Ceuta",
                                "Africa/Conakry",
                                "Africa/Dakar",
                                "Africa/Dar_es_Salaam",
                                "Africa/Djibouti",
                                "Africa/Douala",
                                "Africa/El_Aaiun",
                                "Africa/Freetown",
                                "Africa/Gaborone",
                                "Africa/Harare",
                                "Africa/Johannesburg",
                                "Africa/Juba",
                                "Africa/Kampala",
                                "Africa/Khartoum",
                                "Africa/Kigali",
                                "Africa/Kinshasa",
                                "Africa/Lagos",
                                "Africa/Libreville",
                                "Africa/Lome",
                                "Africa/Luanda",
                                "Africa/Lubumbashi",
                                "Africa/Lusaka",
                                "Africa/Malabo",
                                "Africa/Maputo",
                                "Africa/Maseru",
                                "Africa/Mbabane",
                                "Africa/Mogadishu",
                                "Africa/Monrovia",
                                "Africa/Nairobi",
                                "Africa/Ndjamena",
                                "Africa/Niamey",
                                "Africa/Nouakchott",
                                "Africa/Ouagadougou",
                                "Africa/Porto-Novo",
                                "Africa/Sao_Tome",
                                "Africa/Timbuktu",
                                "Africa/Tripoli",
                                "Africa/Tunis",
                                "Africa/Windhoek",
                                "America/Adak",
                                "America/Anchorage",
                                "America/Anguilla",
                                "America/Antigua",
                                "America/Araguaina",
                                "America/Argentina/Buenos_Aires",
                                "America/Argentina/Catamarca",
                                "America/Argentina/ComodRivadavia",
                                "America/Argentina/Cordoba",
                                "America/Argentina/Jujuy",
                                "America/Argentina/La_Rioja",
                                "America/Argentina/Mendoza",
                                "America/Argentina/Rio_Gallegos",
                                "America/Argentina/Salta",
                                "America/Argentina/San_Juan",
                                "America/Argentina/San_Luis",
                                "America/Argentina/Tucuman",
                                "America/Argentina/Ushuaia",
                                "America/Aruba",
                                "America/Asuncion",
                                "America/Atikokan",
                                "America/Atka",
                                "America/Bahia",
                                "America/Bahia_Banderas",
                                "America/Barbados",
                                "America/Belem",
                                "America/Belize",
                                "America/Blanc-Sablon",
                                "America/Boa_Vista",
                                "America/Bogota",
                                "America/Boise",
                                "America/Buenos_Aires",
                                "America/Cambridge_Bay",
                                "America/Campo_Grande",
                                "America/Cancun",
                                "America/Caracas",
                                "America/Catamarca",
                                "America/Cayenne",
                                "America/Cayman",
                                "America/Chicago",
                                "America/Chihuahua",
                                "America/Coral_Harbour",
                                "America/Cordoba",
                                "America/Costa_Rica",
                                "America/Creston",
                                "America/Cuiaba",
                                "America/Curacao",
                                "America/Danmarkshavn",
                                "America/Dawson",
                                "America/Dawson_Creek",
                                "America/Denver",
                                "America/Detroit",
                                "America/Dominica",
                                "America/Edmonton",
                                "America/Eirunepe",
                                "America/El_Salvador",
                                "America/Ensenada",
                                "America/Fort_Nelson",
                                "America/Fort_Wayne",
                                "America/Fortaleza",
                                "America/Glace_Bay",
                                "America/Godthab",
                                "America/Goose_Bay",
                                "America/Grand_Turk",
                                "America/Grenada",
                                "America/Guadeloupe",
                                "America/Guatemala",
                                "America/Guayaquil",
                                "America/Guyana",
                                "America/Halifax",
                                "America/Havana",
                                "America/Hermosillo",
                                "America/Indiana/Indianapolis",
                                "America/Indiana/Knox",
                                "America/Indiana/Marengo",
                                "America/Indiana/Petersburg",
                                "America/Indiana/Tell_City",
                                "America/Indiana/Vevay",
                                "America/Indiana/Vincennes",
                                "America/Indiana/Winamac",
                                "America/Indianapolis",
                                "America/Inuvik",
                                "America/Iqaluit",
                                "America/Jamaica",
                                "America/Jujuy",
                                "America/Juneau",
                                "America/Kentucky/Louisville",
                                "America/Kentucky/Monticello",
                                "America/Knox_IN",
                                "America/Kralendijk",
                                "America/La_Paz",
                                "America/Lima",
                                "America/Los_Angeles",
                                "America/Louisville",
                                "America/Lower_Princes",
                                "America/Maceio",
                                "America/Managua",
                                "America/Manaus",
                                "America/Marigot",
                                "America/Martinique",
                                "America/Matamoros",
                                "America/Mazatlan",
                                "America/Mendoza",
                                "America/Menominee",
                                "America/Merida",
                                "America/Metlakatla",
                                "America/Mexico_City",
                                "America/Miquelon",
                                "America/Moncton",
                                "America/Monterrey",
                                "America/Montevideo",
                                "America/Montreal",
                                "America/Montserrat",
                                "America/Nassau",
                                "America/New_York",
                                "America/Nipigon",
                                "America/Nome",
                                "America/Noronha",
                                "America/North_Dakota/Beulah",
                                "America/North_Dakota/Center",
                                "America/North_Dakota/New_Salem",
                                "America/Ojinaga",
                                "America/Panama",
                                "America/Pangnirtung",
                                "America/Paramaribo",
                                "America/Phoenix",
                                "America/Port_of_Spain",
                                "America/Port-au-Prince",
                                "America/Porto_Acre",
                                "America/Porto_Velho",
                                "America/Puerto_Rico",
                                "America/Punta_Arenas",
                                "America/Rainy_River",
                                "America/Rankin_Inlet",
                                "America/Recife",
                                "America/Regina",
                                "America/Resolute",
                                "America/Rio_Branco",
                                "America/Rosario",
                                "America/Santa_Isabel",
                                "America/Santarem",
                                "America/Santiago",
                                "America/Santo_Domingo",
                                "America/Sao_Paulo",
                                "America/Scoresbysund",
                                "America/Shiprock",
                                "America/Sitka",
                                "America/St_Barthelemy",
                                "America/St_Johns",
                                "America/St_Kitts",
                                "America/St_Lucia",
                                "America/St_Thomas",
                                "America/St_Vincent",
                                "America/Swift_Current",
                                "America/Tegucigalpa",
                                "America/Thule",
                                "America/Thunder_Bay",
                                "America/Tijuana",
                                "America/Toronto",
                                "America/Tortola",
                                "America/Vancouver",
                                "America/Virgin",
                                "America/Whitehorse",
                                "America/Winnipeg",
                                "America/Yakutat",
                                "America/Yellowknife",
                                "Antarctica/Casey",
                                "Antarctica/Davis",
                                "Antarctica/DumontDUrville",
                                "Antarctica/Macquarie",
                                "Antarctica/Mawson",
                                "Antarctica/McMurdo",
                                "Antarctica/Palmer",
                                "Antarctica/Rothera",
                                "Antarctica/South_Pole",
                                "Antarctica/Syowa",
                                "Antarctica/Troll",
                                "Antarctica/Vostok",
                                "Arctic/Longyearbyen",
                                "Asia/Aden",
                                "Asia/Almaty",
                                "Asia/Amman",
                                "Asia/Anadyr",
                                "Asia/Aqtau",
                                "Asia/Aqtobe",
                                "Asia/Ashgabat",
                                "Asia/Ashkhabad",
                                "Asia/Atyrau",
                                "Asia/Baghdad",
                                "Asia/Bahrain",
                                "Asia/Baku",
                                "Asia/Bangkok",
                                "Asia/Barnaul",
                                "Asia/Beirut",
                                "Asia/Bishkek",
                                "Asia/Brunei",
                                "Asia/Calcutta",
                                "Asia/Chita",
                                "Asia/Choibalsan",
                                "Asia/Chongqing",
                                "Asia/Chungking",
                                "Asia/Colombo",
                                "Asia/Dacca",
                                "Asia/Damascus",
                                "Asia/Dhaka",
                                "Asia/Dili",
                                "Asia/Dubai",
                                "Asia/Dushanbe",
                                "Asia/Famagusta",
                                "Asia/Gaza",
                                "Asia/Harbin",
                                "Asia/Hebron",
                                "Asia/Ho_Chi_Minh",
                                "Asia/Hong_Kong",
                                "Asia/Hovd",
                                "Asia/Irkutsk",
                                "Asia/Istanbul",
                                "Asia/Jakarta",
                                "Asia/Jayapura",
                                "Asia/Jerusalem",
                                "Asia/Kabul",
                                "Asia/Kamchatka",
                                "Asia/Karachi",
                                "Asia/Kashgar",
                                "Asia/Kathmandu",
                                "Asia/Katmandu",
                                "Asia/Khandyga",
                                "Asia/Kolkata",
                                "Asia/Krasnoyarsk",
                                "Asia/Kuala_Lumpur",
                                "Asia/Kuching",
                                "Asia/Kuwait",
                                "Asia/Macao",
                                "Asia/Macau",
                                "Asia/Magadan",
                                "Asia/Makassar",
                                "Asia/Manila",
                                "Asia/Muscat",
                                "Asia/Novokuznetsk",
                                "Asia/Novosibirsk",
                                "Asia/Omsk",
                                "Asia/Oral",
                                "Asia/Phnom_Penh",
                                "Asia/Pontianak",
                                "Asia/Pyongyang",
                                "Asia/Qatar",
                                "Asia/Qyzylorda",
                                "Asia/Rangoon",
                                "Asia/Riyadh",
                                "Asia/Saigon",
                                "Asia/Sakhalin",
                                "Asia/Samarkand",
                                "Asia/Seoul",
                                "Asia/Shanghai",
                                "Asia/Singapore",
                                "Asia/Srednekolymsk",
                                "Asia/Taipei",
                                "Asia/Tashkent",
                                "Asia/Tbilisi",
                                "Asia/Tehran",
                                "Asia/Tel_Aviv",
                                "Asia/Thimbu",
                                "Asia/Thimphu",
                                "Asia/Tokyo",
                                "Asia/Tomsk",
                                "Asia/Ujung_Pandang",
                                "Asia/Ulaanbaatar",
                                "Asia/Ulan_Bator",
                                "Asia/Urumqi",
                                "Asia/Ust-Nera",
                                "Asia/Vientiane",
                                "Asia/Vladivostok",
                                "Asia/Yakutsk",
                                "Asia/Yangon",
                                "Asia/Yekaterinburg",
                                "Asia/Yerevan",
                                "Atlantic/Azores",
                                "Atlantic/Bermuda",
                                "Atlantic/Canary",
                                "Atlantic/Cape_Verde",
                                "Atlantic/Faeroe",
                                "Atlantic/Faroe",
                                "Atlantic/Jan_Mayen",
                                "Atlantic/Madeira",
                                "Atlantic/Reykjavik",
                                "Atlantic/South_Georgia",
                                "Atlantic/St_Helena",
                                "Atlantic/Stanley",
                                "Australia/ACT",
                                "Australia/Adelaide",
                                "Australia/Brisbane",
                                "Australia/Broken_Hill",
                                "Australia/Canberra",
                                "Australia/Currie",
                                "Australia/Darwin",
                                "Australia/Eucla",
                                "Australia/Hobart",
                                "Australia/LHI",
                                "Australia/Lindeman",
                                "Australia/Lord_Howe",
                                "Australia/Melbourne",
                                "Australia/North",
                                "Australia/NSW",
                                "Australia/Perth",
                                "Australia/Queensland",
                                "Australia/South",
                                "Australia/Sydney",
                                "Australia/Tasmania",
                                "Australia/Victoria",
                                "Australia/West",
                                "Australia/Yancowinna",
                                "Brazil/Acre",
                                "Brazil/DeNoronha",
                                "Brazil/East",
                                "Brazil/West",
                                "Canada/Atlantic",
                                "Canada/Central",
                                "Canada/Eastern",
                                "Canada/Mountain",
                                "Canada/Newfoundland",
                                "Canada/Pacific",
                                "Canada/Saskatchewan",
                                "Canada/Yukon",
                                "CET",
                                "Chile/Continental",
                                "Chile/EasterIsland",
                                "CST6CDT",
                                "Cuba",
                                "EET",
                                "Egypt",
                                "Eire",
                                "EST",
                                "EST5EDT",
                                "Etc/GMT",
                                "Etc/GMT+0",
                                "Etc/GMT+1",
                                "Etc/GMT+10",
                                "Etc/GMT+11",
                                "Etc/GMT+12",
                                "Etc/GMT+2",
                                "Etc/GMT+3",
                                "Etc/GMT+4",
                                "Etc/GMT+5",
                                "Etc/GMT+6",
                                "Etc/GMT+7",
                                "Etc/GMT+8",
                                "Etc/GMT+9",
                                "Etc/GMT0",
                                "Etc/GMT-0",
                                "Etc/GMT-1",
                                "Etc/GMT-10",
                                "Etc/GMT-11",
                                "Etc/GMT-12",
                                "Etc/GMT-13",
                                "Etc/GMT-14",
                                "Etc/GMT-2",
                                "Etc/GMT-3",
                                "Etc/GMT-4",
                                "Etc/GMT-5",
                                "Etc/GMT-6",
                                "Etc/GMT-7",
                                "Etc/GMT-8",
                                "Etc/GMT-9",
                                "Etc/Greenwich",
                                "Etc/UCT",
                                "Etc/Universal",
                                "Etc/UTC",
                                "Etc/Zulu",
                                "Europe/Amsterdam",
                                "Europe/Andorra",
                                "Europe/Astrakhan",
                                "Europe/Athens",
                                "Europe/Belfast",
                                "Europe/Belgrade",
                                "Europe/Sarajevo",
                                "Europe/Berlin",
                                "Europe/Bratislava",
                                "Europe/Brussels",
                                "Europe/Bucharest",
                                "Europe/Budapest",
                                "Europe/Busingen",
                                "Europe/Chisinau",
                                "Europe/Copenhagen",
                                "Europe/Dublin",
                                "Europe/Gibraltar",
                                "Europe/Guernsey",
                                "Europe/Helsinki",
                                "Europe/Isle_of_Man",
                                "Europe/Istanbul",
                                "Europe/Jersey",
                                "Europe/Kaliningrad",
                                "Europe/Kiev",
                                "Europe/Kirov",
                                "Europe/Lisbon",
                                "Europe/Ljubljana",
                                "Europe/London",
                                "Europe/Luxembourg",
                                "Europe/Madrid",
                                "Europe/Malta",
                                "Europe/Mariehamn",
                                "Europe/Minsk",
                                "Europe/Monaco",
                                "Europe/Moscow",
                                "Asia/Nicosia",
                                "Europe/Oslo",
                                "Europe/Paris",
                                "Europe/Podgorica",
                                "Europe/Prague",
                                "Europe/Riga",
                                "Europe/Rome",
                                "Europe/Samara",
                                "Europe/San_Marino",
                                "Europe/Sarajevo",
                                "Europe/Saratov",
                                "Europe/Simferopol",
                                "Europe/Skopje",
                                "Europe/Sofia",
                                "Europe/Stockholm",
                                "Europe/Tallinn",
                                "Europe/Tirane",
                                "Europe/Tiraspol",
                                "Europe/Ulyanovsk",
                                "Europe/Uzhgorod",
                                "Europe/Vaduz",
                                "Europe/Vatican",
                                "Europe/Vienna",
                                "Europe/Vilnius",
                                "Europe/Volgograd",
                                "Europe/Warsaw",
                                "Europe/Zagreb",
                                "Europe/Zaporozhye",
                                "Europe/Zurich",
                                "GB",
                                "GB-Eire",
                                "GMT",
                                "GMT+0",
                                "GMT0",
                                "GMT-0",
                                "Greenwich",
                                "Hongkong",
                                "HST",
                                "Iceland",
                                "Indian/Antananarivo",
                                "Indian/Chagos",
                                "Indian/Christmas",
                                "Indian/Cocos",
                                "Indian/Comoro",
                                "Indian/Kerguelen",
                                "Indian/Mahe",
                                "Indian/Maldives",
                                "Indian/Mauritius",
                                "Indian/Mayotte",
                                "Indian/Reunion",
                                "Iran",
                                "Israel",
                                "Jamaica",
                                "Japan",
                                "Kwajalein",
                                "Libya",
                                "MET",
                                "Mexico/BajaNorte",
                                "Mexico/BajaSur",
                                "Mexico/General",
                                "MST",
                                "MST7MDT",
                                "Navajo",
                                "NZ",
                                "NZ-CHAT",
                                "Pacific/Apia",
                                "Pacific/Auckland",
                                "Pacific/Bougainville",
                                "Pacific/Chatham",
                                "Pacific/Chuuk",
                                "Pacific/Easter",
                                "Pacific/Efate",
                                "Pacific/Enderbury",
                                "Pacific/Fakaofo",
                                "Pacific/Fiji",
                                "Pacific/Funafuti",
                                "Pacific/Galapagos",
                                "Pacific/Gambier",
                                "Pacific/Guadalcanal",
                                "Pacific/Guam",
                                "Pacific/Honolulu",
                                "Pacific/Johnston",
                                "Pacific/Kiritimati",
                                "Pacific/Kosrae",
                                "Pacific/Kwajalein",
                                "Pacific/Majuro",
                                "Pacific/Marquesas",
                                "Pacific/Midway",
                                "Pacific/Nauru",
                                "Pacific/Niue",
                                "Pacific/Norfolk",
                                "Pacific/Noumea",
                                "Pacific/Pago_Pago",
                                "Pacific/Palau",
                                "Pacific/Pitcairn",
                                "Pacific/Pohnpei",
                                "Pacific/Ponape",
                                "Pacific/Port_Moresby",
                                "Pacific/Rarotonga",
                                "Pacific/Saipan",
                                "Pacific/Samoa",
                                "Pacific/Tahiti",
                                "Pacific/Tarawa",
                                "Pacific/Tongatapu",
                                "Pacific/Truk",
                                "Pacific/Wake",
                                "Pacific/Wallis"
                        ]
                }
        },
        "foreign_key": {
                "join": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/foreign_key?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "outer_only": {
                "join": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 3,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/outer_only?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "relationship": {
                "join": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 3,
                        "default_value": "many_to_one",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/relationship?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "many_to_one",
                                "many_to_many",
                                "one_to_many",
                                "one_to_one"
                        ]
                }
        },
        "required_joins": {
                "join": {
                        "type": "list_unquoted",
                        "subtype": "view-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/required_joins?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_foreign_key": {
                "join": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/sql_foreign_key?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_on": {
                "join": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/sql_on?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_where": {
                "join": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/join/sql_where?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "query": {
                "aggregate_table": {
                        "type": "anonymous_construct",
                        "subtype": "anonymous_construct",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/aggregate_table/query?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "explore": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "Not documented as child of explore, see https://docs.looker.com/reference/explore-params/aggregate_table?version=7.14&lookml=new#query ",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "materialization": {
                "aggregate_table": {
                        "type": "anonymous_construct",
                        "subtype": "anonymous_construct",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/aggregate_table/materialization?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "dimensions": {
                "query": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/dimensions?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "measures": {
                "query": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/measures?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "pivots": {
                "query": {
                        "type": "list_unquoted",
                        "subtype": "field-ref",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/query/pivots?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "url": {
                "application": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/application/url?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "visualization": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/visualization?version=7.18&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "action": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/action/url?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "map_layer": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/url?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "remote_dependency": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/remote_dependency?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "link": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/field-params/link?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "file": {
                "application": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/application/file?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "visualization": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/visualization?version=7.18&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "map_layer": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/file?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "entitlements": {
                "application": {
                        "type": "anonymous_construct",
                        "subtype": "anonymous_construct",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/application/entitlements?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "local_storage": {
                "entitlements": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 3,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/local_storage?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "navigation": {
                "entitlements": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 3,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/navigation?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "new_window": {
                "entitlements": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 3,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/new_window?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "allow_forms": {
                "entitlements": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 3,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/allow_forms?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "allow_same_origin": {
                "entitlements": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 3,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/allow_same_origin?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "core_api_methods": {
                "entitlements": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/core_api_methods?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "external_api_urls": {
                "entitlements": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/external_api_urls?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "oauth2_urls": {
                "entitlements": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/oauth2_urls?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "global_user_attributes": {
                "entitlements": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/global_user_attributes?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "scoped_user_attributes": {
                "entitlements": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/entitlements/scoped_user_attributes?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "id": {
                "visualization": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/visualization?version=7.18&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sri_hash": {
                "visualization": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/visualization?version=7.18&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "dependencies": {
                "visualization": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/visualization?version=7.18&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "icon_url": {
                "action": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/action/icon_url?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "link": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/field-params/link?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "form_url": {
                "action": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/action/form_url?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "param": {
                "action": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/action/param?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "form_param": {
                "action": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/action/form_param?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "user_attribute_param": {
                "action": {
                        "type": "anonymous_construct",
                        "subtype": "anonymous_construct",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/action/user_attribute_param?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "name": {
                "form_param": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/form_param/name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "option": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 5,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/option/name?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "param": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/field-params/action?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "user_attribute_param": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/field-params/action?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "option": {
                "form_param": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/form_param/option?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "required": {
                "form_param": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 4,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/form_param/required?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "default": {
                "form_param": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/form_param/default?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "when": {
                "case": {
                        "type": "anonymous_construct_plural",
                        "subtype": "anonymous_construct_plural",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/case/when?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "else": {
                "case": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/case/else?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "field": {
                "column": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 5,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/column/field?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "access_filter": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/explore-params/access_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "from_field": {
                "bind_filters": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 5,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/bind_filters/from_field?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "to_field": {
                "bind_filters": {
                        "type": "string_unquoted",
                        "subtype": "field-ref",
                        "indent": 5,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/bind_filters/to_field?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "extents_json_url": {
                "map_layer": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/extents_json_url?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "feature_key": {
                "map_layer": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/feature_key?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "format": {
                "map_layer": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 1,
                        "default_value": "topojson",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/format?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "topojson",
                                "vector_tile_region"
                        ]
                }
        },
        "max_zoom_level": {
                "map_layer": {
                        "type": "string_unquoted",
                        "subtype": "number",
                        "indent": 1,
                        "default_value": "12",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/max_zoom_level?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "min_zoom_level": {
                "map_layer": {
                        "type": "string_unquoted",
                        "subtype": "number",
                        "indent": 1,
                        "default_value": "2",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/min_zoom_level?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "projection": {
                "map_layer": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 1,
                        "default_value": "airy",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/projection?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "airy",
                                "aitoff",
                                "albers",
                                "albersUsa",
                                "armadillo",
                                "august",
                                "azimuthalEqualArea",
                                "azimuthalEquidistant",
                                "baker",
                                "berghaus",
                                "boggs",
                                "bonne",
                                "bromley",
                                "chamberlin",
                                "collignon",
                                "conicConformal",
                                "conicEqualArea",
                                "conicEquidistant",
                                "craig",
                                "craster",
                                "cylindricalEqualArea",
                                "cylindricalStereographic",
                                "eckert1",
                                "eckert2",
                                "eckert3",
                                "eckert4",
                                "eckert5",
                                "eckert6",
                                "eisenlohr",
                                "equirectangular",
                                "fahey",
                                "foucaut",
                                "gilbert",
                                "ginzburg4",
                                "ginzburg5",
                                "ginzburg6",
                                "ginzburg8",
                                "ginzburg9",
                                "gnomonic",
                                "gringorten",
                                "guyou",
                                "hammer",
                                "hammerRetroazimuthal",
                                "hatano",
                                "healpix",
                                "hill",
                                "homolosine",
                                "kavrayskiy7",
                                "lagrange",
                                "larrivee",
                                "laskowski",
                                "littrow",
                                "loximuthal",
                                "mercator",
                                "miller",
                                "modifiedStereographic",
                                "mollweide",
                                "mtFlatPolarParabolic",
                                "mtFlatPolarQuartic",
                                "mtFlatPolarSinusoidal",
                                "naturalEarth",
                                "nellHammer",
                                "orthographic",
                                "peirceQuincuncial",
                                "polyconic",
                                "rectangularPolyconic",
                                "robinson",
                                "satellite",
                                "sinuMollweide",
                                "sinusoidal",
                                "stereographic",
                                "times",
                                "transverseMercator",
                                "twoPointAzimuthal",
                                "twoPointEquidistant",
                                "vanDerGrinten",
                                "vanDerGrinten2",
                                "vanDerGrinten3",
                                "vanDerGrinten4",
                                "wagner4",
                                "wagner6",
                                "wagner7",
                                "wiechel",
                                "winkel3",
                                "cartesian"
                        ]
                }
        },
        "property_key": {
                "map_layer": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/property_key?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "property_label_key": {
                "map_layer": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/map_layer/property_label_key?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "assert": {
                "test": {
                        "type": "named_construct",
                        "subtype": "identifier",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/test/assert?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "max_cache_age": {
                "datagroup": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/datagroup/max_cache_age?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_trigger": {
                "datagroup": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/datagroup/sql_trigger?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "strict_value_format": {
                "named_value_format": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 1,
                        "default_value": "no",
                        "docs_url": "https://looker.com/docs/r/lookml/types/named_value_format/strict_value_format?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "allowed_values": {
                "access_grant": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/access_grant/allowed_values?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "user_attribute": {
                "access_grant": {
                        "type": "string_unquoted",
                        "subtype": "user-attribute-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/access_grant/user_attribute?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "user_attribute_param": {
                        "type": "string_unquoted",
                        "subtype": "user-attribute-ref",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/field-params/action?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "access_filter": {
                        "type": "string_unquoted",
                        "subtype": "user-attribute-ref",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/explore-params/access_filter?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "sql_step": {
                "create_process": {
                        "type": "sql",
                        "subtype": "sql-block ",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/view-params/create_process?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "ref": {
                "remote_dependency": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/remote_dependency?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "override_constant": {
                "remote_dependency": {
                        "type": "named_construct",
                        "subtype": "constant-ref",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/remote_dependency?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "value": {
                "override_constant": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/data-modeling/learning-lookml/importing-projects?version=7.14&lookml=new#passing_constants_between_projects",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "param": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 4,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/field-params/action?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "constant": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/constant?version=7.14&lookml=new#using_export_in_imported_projects",
                        "has_allowed_values": False,
                        "allowed_values": ""
                },
                "allowed_value": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/field-params/parameter?version=7.14&lookml=new#specifying_allowed_values",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "new_window_external_urls": {
                "entitlements": {
                        "type": "list_quoted",
                        "subtype": "list_quoted",
                        "indent": 3,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/application?version=7.18&lookml=new#new_window",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "use_form_submit": {
                "entitlements": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 3,
                        "default_value": "no",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/application?version=7.18&lookml=new#use_form_submit",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "use_embeds": {
                "entitlements": {
                        "type": "yesno",
                        "subtype": "yesno",
                        "indent": 3,
                        "default_value": "no",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/application?version=7.18&lookml=new#use_embeds",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "project": {
                "local_dependency": {
                        "type": "string",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "",
                        "docs_url": "https://looker.com/docs/r/lookml/types/manifest/local_dependency?version=7.14&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "export": {
                "constant": {
                        "type": "options",
                        "subtype": "string",
                        "indent": 2,
                        "default_value": "none",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/constant?version=7.14&lookml=new#using_export_in_imported_projects",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "none",
                                "override_required",
                                "override_optional"
                        ]
                }
        },
        "visualization": {
                "manifest": {
                        "type": "anonymous_construct_plural",
                        "subtype": "string",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/visualization?version=7.18&lookml=new",
                        "has_allowed_values": False,
                        "allowed_values": ""
                }
        },
        "default_locale": {
                "localization_settings": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 1,
                        "default_value": "",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/localization_settings?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "ar_AE",
                                "ar_JO",
                                "ar_SY",
                                "hr_HR",
                                "fr_BE",
                                "es_PA",
                                "mt_MT",
                                "es_VE",
                                "bg",
                                "zh_TW",
                                "it",
                                "ko",
                                "uk",
                                "lv",
                                "da_DK",
                                "es_PR",
                                "vi_VN",
                                "en_US",
                                "sr_ME",
                                "sv_SE",
                                "es_BO",
                                "en_SG",
                                "ar_BH",
                                "pt",
                                "ar_SA",
                                "sk",
                                "ar_YE",
                                "hi_IN",
                                "ga",
                                "en_MT",
                                "fi_FI",
                                "et",
                                "sv",
                                "cs",
                                "sr_BA_#Latn",
                                "el",
                                "uk_UA",
                                "hu",
                                "fr_CH",
                                "in",
                                "es_AR",
                                "ar_EG",
                                "ja_JP_JP_#u-ca-japanese",
                                "es_SV",
                                "pt_BR",
                                "be",
                                "is_IS",
                                "cs_CZ",
                                "es",
                                "pl_PL",
                                "tr",
                                "ca_ES",
                                "sr_CS",
                                "ms_MY",
                                "hr",
                                "lt",
                                "es_ES",
                                "es_CO",
                                "bg_BG",
                                "sq",
                                "fr",
                                "ja",
                                "sr_BA",
                                "is",
                                "es_PY",
                                "de",
                                "es_EC",
                                "es_US",
                                "ar_SD",
                                "en",
                                "ro_RO",
                                "en_PH",
                                "ca",
                                "ar_TN",
                                "sr_ME_#Latn",
                                "es_GT",
                                "sl",
                                "ko_KR",
                                "el_CY",
                                "es_MX",
                                "ru_RU",
                                "es_HN",
                                "zh_HK",
                                "no_NO_NY",
                                "hu_HU",
                                "th_TH",
                                "ar_IQ",
                                "es_CL",
                                "fi",
                                "ar_MA",
                                "ga_IE",
                                "mk",
                                "tr_TR",
                                "et_EE",
                                "ar_QA",
                                "sr__#Latn",
                                "pt_PT",
                                "fr_LU",
                                "ar_OM",
                                "th",
                                "sq_AL",
                                "es_DO",
                                "es_CU",
                                "ar",
                                "ru",
                                "en_NZ",
                                "sr_RS",
                                "de_CH",
                                "es_UY",
                                "ms",
                                "el_GR",
                                "iw_IL",
                                "en_ZA",
                                "th_TH_TH_#u-nu-thai",
                                "hi",
                                "fr_FR",
                                "de_AT",
                                "nl",
                                "no_NO",
                                "en_AU",
                                "vi",
                                "nl_NL",
                                "fr_CA",
                                "lv_LV",
                                "de_LU",
                                "es_CR",
                                "ar_KW",
                                "sr",
                                "ar_LY",
                                "mt",
                                "it_CH",
                                "da",
                                "de_DE",
                                "ar_DZ",
                                "sk_SK",
                                "lt_LT",
                                "it_IT",
                                "en_IE",
                                "zh_SG",
                                "ro",
                                "en_CA",
                                "nl_BE",
                                "no",
                                "pl",
                                "zh_CN",
                                "ja_JP",
                                "de_GR",
                                "sr_RS_#Latn",
                                "iw",
                                "en_IN",
                                "ar_LB",
                                "es_NI",
                                "zh",
                                "mk_MK",
                                "be_BY",
                                "sl_SI",
                                "es_PE",
                                "in_ID",
                                "en_GB"
                        ]
                }
        },
        "localization_level": {
                "localization_settings": {
                        "type": "options",
                        "subtype": "options",
                        "indent": 1,
                        "default_value": "permissive",
                        "docs_url": "https://docs.looker.com/reference/manifest-params/localization_settings?version=7.14&lookml=new",
                        "has_allowed_values": True,
                        "allowed_values": [
                                "permissive",
                                "strict"
                        ]
                }
        }
}