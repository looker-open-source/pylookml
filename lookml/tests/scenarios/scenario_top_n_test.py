import unittest
import lookml

class testTopN(unittest.TestCase):
    def setUp(self):
        pass
    def test_topN(self):
        def apply_top_n(
            project, 
            view_file, 
            view, 
            rank_by_dims, 
            rank_by_meas, 
            model_file, 
            explore, 
            agg_view='rank_ndt', 
            dynamic_dim_name='dynamic_dim', 
            dynamic_dim_selector='dynamic_dim_selector'):
            #### SETUP ####
            p = project
            mf = p[model_file]
            vf = p[view_file]
            v = vf['views'][view]
            e = mf['explores'][explore]
            #### DO WORK ####
            #Add the parameter to the initial view file
            dynamic_dim_sql = ''
            i = 0
            for key,val in rank_by_dims.items():
                if i == 0:
                    dynamic_dim_sql = f"{{% if {v.name}.{dynamic_dim_selector}._parameter_value == '{key}' %}} {val}"
                else:
                    dynamic_dim_sql = dynamic_dim_sql + '\n' + f"{{% elsif {v.name}.{dynamic_dim_selector}._parameter_value == '{key}' %}} {val}"
                i = 1 + 1
            dynamic_dim_sql = dynamic_dim_sql + f"""
                    {{% else %}} 'N/A' 
                    {{% endif %}}
                """
            allowed_values = ''
            for key in rank_by_dims.keys():
                allowed_values = allowed_values + f'allowed_value: {{ label: "{key}" value: "{key}"}}'

            v + f'''
                parameter: {dynamic_dim_selector} {{
                    type: unquoted

                    {allowed_values}
                }}'''

            v + f'''
                dimension: {dynamic_dim_name} {{
                    type: string
                    hidden: yes
                    sql: {dynamic_dim_sql};;
                }}

            '''
            #create the aggregate ndt
            agg = lookml.View(agg_view)
            agg + f'''
                derived_table: {{
                    explore_source: {e.name} {{
                    column: {dynamic_dim_name} {{field: {v.name}.{dynamic_dim_name}}}
                    column: {rank_by_meas} {{field: {v.name}.{rank_by_meas}}}
                    derived_column: rank {{
                        sql: ROW_NUMBER() OVER (ORDER BY {rank_by_meas} DESC) ;;
                    }}
                    # bind_all_filters: yes
                    bind_filters: {{
                        from_field: {v.name}.{dynamic_dim_selector}
                        to_field: {v.name}.{dynamic_dim_selector}
                    }}
                    }}
                }}
                dimension: {dynamic_dim_name} {{
                    sql: ${{TABLE}}.{dynamic_dim_name} ;;
                    hidden: yes
                }}
                dimension: rank {{
                    type: number
                    hidden: yes
                }}
                filter: tail_threshold {{
                    type: number
                    hidden: yes
                }}
                dimension: stacked_rank {{
                    type: string
                    sql:
                            CASE
                            WHEN ${{rank}} < 10 then '0' || ${{rank}} || ') '|| ${{{dynamic_dim_name}}}
                            ELSE ${{rank}} || ') ' || ${{{dynamic_dim_name}}}
                            END
                    ;;
                }}
                dimension: ranked_by_with_tail {{
                    type: string
                    sql:
                        CASE WHEN {{% condition tail_threshold %}} ${{rank}} {{% endcondition %}} THEN ${{stacked_rank}}
                        ELSE 'x) Other'
                        END
                    ;;
                }}
            '''
            #add our new aggregate view to the view file
            vf + agg
            #join in our aggregate table to the explore
            e + f'''
              join: {agg.name} {{
                type: left_outer
                relationship: many_to_one
                sql_on: ${{{v.name}.{dynamic_dim_name}}}  = ${{{agg.name}.{dynamic_dim_name}}};;
             }}
            '''

            #### SAVE ####
            print(vf)
            vf.write()
            mf.write()
            # p.put(vf)
            # p.put(mf)
            p.deploy()
        apply_top_n(
             lookml.Project(**config['project1'])
            ,'order_items.view.lkml' #ordinarily should be my view file
            ,'order_items'
            ,{'Brand':'${products.brand}','Category':'${products.category}','State':'${users.state}'}
            ,'total_sale_price'
            ,'order_items.model.lkml' 
            ,'order_items'
            )