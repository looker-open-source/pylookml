import lookml
import lkml

with open('order_items.view.lkml', 'r') as file:
    parsed = lkml.load(file)

# with open('thelook.model.lkml', 'r') as file:
#     parsed = lkml.load(file)

# f = open("thefile.json", "w")
# f.write(str(parsed))
# f.close()
# print(parsed)

if 'views' in parsed.keys():
    f = list()
    for view in parsed['views']:
        tmpView = lookml.View(view)
        # print(tmpView)
        # print(tmpView)
        # view.pop('name')
        # for dim in view['dimensions']:
        #     tmpDim = lookml.Dimension(dim.pop('name'))
        #     for k,v in dim.items():
        #         tmpDim.setProperty(k,v) 
        #     tmpView + tmpDim
        # for measure in view['measures']:
        #     tmpMeas = lookml.Measure(measure['name'])
        #     for k,v in measure.items():
        #         if k != 'name':
        #             tmpMeas.setProperty(k,v)
        #     tmpView + tmpMeas
        # for flter in view['filters']:
        #     tmpFlt = lookml.Filter(flter['name'])
        #     for k,v in flter.items():
        #         if k != 'name':
        #             tmpFlt.setProperty(k,v)
        #     tmpView + tmpFlt
        # for dim in view['dimension_groups']:
        #     tmpDim = lookml.DimensionGroup(dim['name'])
        #     for k,v in dim.items():
        #         if k != 'name':
        #             tmpDim.setProperty(k,v)
        #     tmpView + tmpDim
# if 'explores' in parsed.keys():
#     for explore in parsed['explores']:
#         tmpExplore = lookml.Explore(**explore)
#         print(tmpExplore)


# tmpView + 'zz'
print(tmpView)


#dimensions
#measures
#filters


#TODO: Make the internal datastructure of the class the JSON.... i.e. as the class state is modified so is the underlying json.

#TODO: Tiers are wierd
#TODO: Name makes sense at some points and levels (KEYS_WITH_NAME_FIELDS = ("user_attribute_param", "param", "form_param", "option")) https://github.com/joshtemple/lkml/commit/676c214fcc0e0641eb353095c6b3de3232df1695
#TODO: Filters within fields/ measures
#TODO: Sets
#TODO: Actions
#TODO: Constants
#TODO: Suggestions
#TODO: Timeframes
#TODO: Programatic Manipulation Tag / comment
#TODO: Project Puller / Github Pull Down (obtain from Bryan)
#TODO: Boilerplate Code for this... [super view example...multi-model example...liveupdate service (lambda / cloud funcitons)] 
#TODO: Common Macros --> i.e. fast blocks 
        # Ideas:
        #  BigQuery table JSON auto creates the LookML
        #  Aggregate Awareness Macro
        #  Auto EAV Unnester
        #  Automatic Creation of NDT for pivot by rank type stuff
        #  Calendar Table
        #  SFDC Waterfall
        #  Guided Star Schema Generation?
        #  Multi Grain period over period 
        #  Drill to vis with constants
        #  Incremental PDTs? --> This breaks as of Looker 7?
        #  Negative Intervals Hacking
        #  Linking macro, Intel linking block?
        #  Fancy Conditional Formatting examples
        #  Something with slowly changing dimensions
#TODO: Interactive block construction macro --> i.e. fast blocks 
#TODO: Massive Documentation
#TODO: Comprehensive and good unit tests
#TODO: Common Sql Functions added to the SQL paramter
#TODO: Common HTML Functions added to the HTML paramter
#TODO: Ontology from the project.file.view.field? project.model.view.field? 
#TODO: Preserve initial ordering?

#Done:
#TODO: Dimension Groups
#TODO: Filters
#TODO: Measures

