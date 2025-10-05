items = context.AffectedItems

for item in items:
    if item['LBF_QU_PLANT1']:
        plant = item['LBF_QU_PLANT1']
        material = item.PartNumber
        query = "select DC, DIV, SORG, Plant from LBF_QU_MAT_COST where Material Like '%{0}' and Plant = '{1}'".format(str(material),str(plant))
        result = SqlHelper.GetFirst(query)
        Log.Info('calling the data - > ' + str(material))
        if result:
            item['LBF_QU_PLANT1'] = result.Plant
            item['LBF_QU_SalesOrg'] = result.SORG
            item['LBF_QU_PLANT'] = result.Plant
            item['LBF_QU_DIV'] = result.DIV if result.DIV else 0
            item['LBF_QU_DC'] = result.DC
            #item['LBF_QU_ITEMDESC'] = item.Description
    else:
        material = item.PartNumber
        query = "select DC, DIV, SORG, Plant from LBF_QU_MAT_COST where Material Like '%{0}'".format(str(material))
        result = SqlHelper.GetFirst(query)
        Log.Info('calling the data - > ' + str(material))
        if result:
            item['LBF_QU_PLANT1'] = result.Plant
            item['LBF_QU_SalesOrg'] = result.SORG
            item['LBF_QU_PLANT'] = result.Plant
            item['LBF_QU_DIV'] = result.DIV if result.DIV else 0
            item['LBF_QU_DC'] = result.DC
            #item['LBF_QU_ITEMDESC'] = item.Description