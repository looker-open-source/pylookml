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




