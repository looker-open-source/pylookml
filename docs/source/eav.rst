AutoGen for EAV
------------------------------

.. warning:: Setting up EAV automation can generate high code volume. Pair with a Looker architect to plan for scale. Multiple instances may be necessary at large volumes. 


************
What is EAV?
************

EAV data is storing key / value pairs in a table. It can allow application owners to hold data for which they can't predict the columns or attributes at design time. 
Common examples might include customizable objects (i.e. my users can add their own fields),or scientific data with many attributes or surveys. 
EAV data allows flexibility, but can be notoriously difficult to perform analysis on. In this tutorial, we will show how pyLookML can be configured to create LookML for unpacking, imposing a permission structure
and allowing analysis on EAV data. 


*An Example of a configurable user profile table*

Our example will follow a site with a configurable user profile. Organizations that use the site "Orgs" can add profile fields for their members so that admins can track org specific values for each of their user accounts. 



Here is the sample data we'll be using throughout. Imagine this sample data comes from a table called custom_profile_fields.

.. csv-table:: custom_profile_fields
   :header: "user_id", "org_id","field_name", "value", "datatype"
   :widths: 8, 8, 20, 20, 20

   1, 8, "c_donation_amount", 40, "int"
   1, 8, "c_highest_achievement", "gold badge", "varchar"
   2, 101, "c_highest_achievement", "silver badge", "varchar"
   2, 101, "c_monthly_contribution", 300, "int"
   3, 101, "c_highest_achievement", "bronze badge", "varchar"
   3, 101, "c_monthly_contribution", 350, "int"
   4, 101, "c_monthly_contribution", 350, "int" 
   4, 101, "age", 32, "int" 
   5, 102, "c_monthly_contribution", 100, "int"

You can see that the field name and value form the key,value relationship characteristic of EAV. Structured in a traditional table layout, we would need 4 columns to capture the 4 distinct custom fields: 
c_donation_amount, c_highest_achievement, c_monthly_contribution, age.  And this would grow (as orgs and user accounts were added) to be much wider than is practical, or wider than the database may even allow a table to be.
However for analysis, we want to create a "slice" of this table for each org, showing them just their attributes as if it were a normal table. 
Also notice that because the "value" column has mixed datatypes it must be a wide and neutral (typically a very wide varchar) and cast by the application when the record is read. Often by necessity you will often see the value paired with a column which tracks its type so the application can bind it to the right datatype at runtime. 


Here is the LookML starting point (the script assumes that you have already created views for the relevant tables) but it will allow the ongoing programatic addition of fields.
We have a usr table which tracks basic information about our user accounts eav_source (which would be pointed at public.custom_profile_fields) and usr_profile which will track the extended profile attributes from custom_profile_fields (we'll also permission the fields at the org level).
The explore usr, just associates our usr table to the usr profile table which will contain the un-packed EAV values. We have also added an access filter, so that our orgs can only see thier own records.

.. code-block:: javascript

    connection: "snowlooker"

    explore: usr {
        access_filter: {
            field: usr_profile.org_id
            user_attribute: org_id
        }
        join: usr_profile {
            type: left_outer
            relationship: one_to_one
            sql_on: ${usr.id} =  ${usr_profile.user_id} ;;
        }
    }

    view: usr {
        sql_table_name: public.users ;;
        dimension: email {}
        dimension: id {}
        dimension_group: created { timeframes: [raw,date,month,year] }
    }

    view: usr_profile {
        dimension: org_id {}
        dimension: user_id {}
    }

    view: eav_source {
        sql_table_name: public.custom_profile_fields ;;
        dimension: datatype { type: string }
        dimension: field_name { type: string }
        dimension: org_id { type: number }
        dimension: user_id { type: number }
        dimension: value { type: string }
    }


Now for the automation code. First install the dependencies (FYI I highly reccoemnd using a virtual environment).
We will be using the `Looker SDK <https://github.com/looker-open-source/sdk-codegen/tree/master/python>`_ to run sql against the DB which will tell us what fields we need to create. 
And we'll install our pyLookML package as well.

.. code-block:: bash

   pip install lookml, looker_sdk

create a file called api.ini in the directory where your python script will run to house the Looker API connection parameters: 

.. code-block:: bash

    # Base URL for API. Do not include /api/* in the url
    base_url = https://mylooker.looker.com:19999
    # API 3 client id
    client_id=put_your_client_id_here
    # API 3 client secret
    client_secret=put_your_sectret_here
    # Set to false if testing locally against self-signed certs. Otherwise leave True



The automation python file follows these high level steps.

    1. connect to the Looker API to pull a list of EAV fields
    2. create a pyLookML project connection to your github
    3. Set up the objects we'll be manipulating (some are just strings which will be added back to the LookML at the end)
    4. loop over the list of EAV k,v pairs and do work
    5. loop over the distinct raw columns (obtained in the full k,v loop) for adding columns to the NDT
    6. loop over the distinct org ids to add the model's access grants
    7. add all the final objects back to the model file
    8. save the file back to the project in github 
    9. hit the looker deploy URL to sync Looker production mode with the github master branch

.. code-block:: python
   :linenos:

    import lookml
    from looker_sdk import models, methods, init40
    import json

    # step 1 -- connect to the Looker API to pull a list of EAV fields
    sdk = init40("api.ini")
    sql_for_fields = f"""
            SELECT
                cpf.org_id
                ,cpf.value
                ,cpf.datatype
                ,cpf.field_name as FIELD_NAME
                , CASE
                    WHEN cpf.datatype IN ('TIMESTAMP_LTZ') THEN 'time'
                    WHEN cpf.datatype IN ('FLOAT','NUMBER', 'int') THEN 'number'
                    ELSE 'string' END as LOOKER_TYPE
            FROM
                -- public.custom_profile_fields as cpf
                (
                    SELECT 1 as user_id, 8 as org_id, 'c_donation_amount' as field_name, '40' as value, 'int' as datatype UNION ALL
                    SELECT 1, 8, 'c_highest_achievement', 'gold badge', 'varchar' UNION ALL
                    SELECT 2, 101, 'c_highest_achievement', 'silver badge', 'varchar' UNION ALL
                    SELECT 2, 101, 'c_monthly_contribution', '300', 'int' UNION ALL
                    SELECT 3, 101, 'c_highest_achievement', 'bronze badge', 'varchar' UNION ALL
                    SELECT 3, 101, 'c_monthly_contribution', '350', 'int' UNION ALL
                    SELECT 4, 101, 'c_monthly_contribution', '350', 'int' UNION ALL
                    SELECT 4, 101, 'age', '32', 'int' UNION ALL
                    SELECT 5, 102, 'c_monthly_contribution', '100', 'int'
                ) as cpf
            WHERE
                1=1
            GROUP BY 1,2,3,4,5
    """
    query_config = models.SqlQueryCreate(sql=sql_for_fields, connection_id="snowlooker")
    query = sdk.create_sql_query(query_config)
    response = json.loads(sdk.run_sql_query(slug=query.slug, result_format="json"))

    # step 2 -- create a pyLookML project connection to your github
    proj = lookml.Project(
            #the github location of the repo
            repo= 'llooker/your_repo'
            #instructions on creating an access token: https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
            ,access_token='your_access_token'
            #your Looker host
            ,looker_host="https://example.looker.com/"
            #The name of the project on your looker host
            ,looker_project_name="pylookml_testing_2"
            #You can deploy to branches other than master, a shared or personal branch if you would like to hop into looker, pull
            #remote changes and review before the code is committed to production
            ,branch='master'
    )
    #For simplicity of this example, all of the objects we're tracking will be contained in the model file, but for your needs can be split across the project.
    modelFile = proj['eav_model.model.lkml']

    # step 3 -- Set up the objects we'll be manipulating (some are just strings which will be added back to the LookML at the end)
    #the EAV source view points to our custom_profile_fields database table
    eavSource = modelFile['views']['eav_source']
    #the user profile we'll call the "flattening NDT" since that's where our flattening logic lives
    flatteningNDT = modelFile['views']['usr_profile']


    #Ensure there is a hidden explore to expose the eav_souce transformations to our user_profile NDT
    modelFile + f'''
        explore: _eav_flattener {{
            from: {eavSource.name}
            hidden: yes
        }}
    '''
    #Begin the derived table, will be added to as we loop through the fields
    drivedtableString = f'''
        derived_table: {{
            explore_source: _eav_flattener {{
                column: user_id {{ field: _eav_flattener.user_id }}
                column: org_id {{ field: _eav_flattener.org_id }}
    '''

    #Set up a pair of list to track the unique org ids and column names
    #since the api query will be at a org / column level this allows us to "de-dupe"
    orgIds, columns = [], []

    # step 4 -- loop over the list of EAV k,v pairs and do work
    for column in response:
        dimName = lookml.core.lookCase(column['FIELD_NAME'])
        orgIds.append(column['org_id'])
        columns.append(dimName)
        #Step 1) Add flattening measure to the EAV source table
        eavSource + f'''
                measure: {dimName} {{
                    type: max
                    sql: CASE WHEN ${{field_name}} = '{column['FIELD_NAME']}' THEN ${{value}} ELSE NULL END;;
                }}
        '''

        # Add to the NDT fields
        flatteningNDT + f'''
                dimension: {dimName}_org_{column['org_id']} {{
                    label: "{dimName}"
                    type: {column['LOOKER_TYPE']}
                    sql: ${{TABLE}}.{dimName} ;;
                    required_access_grants: [org_{column['org_id']}]
                }}
        '''
        if column['LOOKER_TYPE'] == "number":
            flatteningNDT + f'''
                measure: {dimName}_total_org_{column['org_id']} {{
                    label: "{dimName}_total"
                    type: sum
                    sql: ${{{dimName}_org_{column['org_id']}}} ;;
                    required_access_grants: [org_{column['org_id']}]
                }}
            '''
    # step 5 -- loop over the distinct raw columns (obtained in the full k,v loop) for adding columns to the NDT
    for col in set(columns):
        drivedtableString += f' column: {col} {{ field: _eav_flattener.{col} }}'
    drivedtableString += '}}'

    # step 6 -- loop over the distinct org ids to add the model's access grants
    accessGrants = ''
    for org in set(orgIds):
        accessGrants += f'''
            access_grant: org_{org} {{
            user_attribute: org_id
            allowed_values: [
                "{org}"
            ]
            }}
        '''
    # step 7 -- add all the final objects back to the model file
    #Finish by adding some of the strings we've been tracking:
    flatteningNDT + drivedtableString
    #Add access grants to the model
    modelFile + accessGrants

    # step 8 -- save the file back to the project in github
    proj.put(modelFile)
    #s step 9 -- hit the looker deploy URL to sync Looker production mode with the github master branch
    proj.deploy()


The Completed LookML output to the eav.model.lkml file

.. code-block:: javascript

    connection: "snowlooker"

    access_grant: org_8 {
        user_attribute: org_id
        allowed_values: [
            "8",
        ]
    }
    access_grant: org_101 {
        user_attribute: org_id
        allowed_values: [
            "101",
        ]
    }
    access_grant: org_102 {
        user_attribute: org_id
        allowed_values: [
            "102",
        ]
    }

    explore: usr {
        access_filter: {
            field: usr_profile.org_id
            user_attribute: org_id
        }
        join: usr_profile {
            type: left_outer
            relationship: one_to_one
            sql_on: ${usr.id} =  ${usr_profile.user_id} ;; 
        }
    }

    explore: _eav_flattener {
        from: eav_source
        hidden: yes
    }

    view: usr {
        sql_table_name: public.users ;;
        dimension: email {}
        dimension: id {}
        dimension_group: created {
            timeframes: [
                raw, date, month, year,
            ]
            type: time
            }
    }

    view: usr_profile {
    
    derived_table: {
        explore_source: _eav_flattener {
        column: user_id { field: _eav_flattener.user_id}
        column: org_id { field: _eav_flattener.org_id }
        column: c_donation_amount { field: _eav_flattener.c_donation_amount}
        column: c_monthly_contribution { field: _eav_flattener.c_monthly_contribution }
        column: c_highest_achievement { field: _eav_flattener.c_highest_achievement }
        column: age { field: _eav_flattener.age }
        }
    }
    dimension: age_org_101 {
        label: "age"
        type: number
        sql: ${TABLE}.age ;;
        required_access_grants: [org_101,] 
        }
    dimension: c_donation_amount_org_8 {
        label: "c_donation_amount"
        type: number
        sql: ${TABLE}.c_donation_amount ;;
        required_access_grants: [org_8,] 
        }
    dimension: c_highest_achievement_org_101 {
        label: "c_highest_achievement"
        type: string
        sql: ${TABLE}.c_highest_achievement ;;
        required_access_grants: [org_101,] 
        }
    dimension: c_highest_achievement_org_8 {
        label: "c_highest_achievement"
        type: string
        sql: ${TABLE}.c_highest_achievement ;;
        required_access_grants: [org_8,]
        }
    dimension: c_monthly_contribution_org_101 {
        label: "c_monthly_contribution"
        type: number
        sql: ${TABLE}.c_monthly_contribution ;;
        required_access_grants: [org_101,] 
        }
    dimension: c_monthly_contribution_org_102 {
        label: "c_monthly_contribution"
        type: number
        sql: ${TABLE}.c_monthly_contribution ;;
        required_access_grants: [org_102,] 
        }
    dimension: org_id {}
    dimension: user_id {}
    measure: age_total_org_101 {
        label: "age_total"
        type: sum
        sql: ${age_org_101} ;;
        required_access_grants: [org_101,] 
        }
    measure: c_donation_amount_total_org_8 {
        label: "c_donation_amount_total"
        type: sum
        sql: ${c_donation_amount_org_8} ;;
        required_access_grants: [org_8,] 
        }
    measure: c_monthly_contribution_total_org_101 {
        label: "c_monthly_contribution_total"
        type: sum
        sql: ${c_monthly_contribution_org_101} ;;
        required_access_grants: [org_101,] 
        }
    measure: c_monthly_contribution_total_org_102 {
        label: "c_monthly_contribution_total"
        type: sum
        sql: ${c_monthly_contribution_org_102} ;;
        required_access_grants: [org_102,] 
        }
    }

    view: eav_source {
    sql_table_name: public.custom_profile_fields ;;
    dimension: datatype { type: string }
    dimension: field_name { type: string }
    dimension: org_id { type: number }
    dimension: user_id { type: number }
    dimension: value { type: string }

    measure: age {
        type: max
        sql: CASE WHEN ${field_name} = 'age' THEN ${value} ELSE NULL END ;; 
        }
    measure: c_donation_amount {
        type: max
        sql: CASE WHEN ${field_name} = 'c_donation_amount' THEN ${value} ELSE NULL END ;; 
        }
    measure: c_highest_achievement {
        type: max
        sql: CASE WHEN ${field_name} = 'c_highest_achievement' THEN ${value} ELSE NULL END ;; 
        }
    measure: c_monthly_contribution {
        type: max
        sql: CASE WHEN ${field_name} = 'c_monthly_contribution' THEN ${value} ELSE NULL END ;; 
        }
    }



More information and resources
*******************************
    1. `2019 Looker JOIN presentation on EAV and LookML Generation <https://www.youtube.com/watch?v=cdyn-KLwyfc>`_
    2. `More about modeling EAV data in Looker <https://discourse.looker.com/t/three-ways-to-model-eav-schemas-and-many-to-many-relationships/1780>`_ 

As an alternative to the MAX(CASE WHEN NAME='foo' THEN VALUE END) construct, you can use first / last value window functions. The specifics of the implementation may look slightly different.

.. code-block:: sql

            FIRST_VALUE(
                CASE
                    WHEN attributename = 'single_type' THEN attributevalue
                    ELSE NULL
                END
            IGNORE NULLS)
            OVER (partition by sessionid order by sessionid)
