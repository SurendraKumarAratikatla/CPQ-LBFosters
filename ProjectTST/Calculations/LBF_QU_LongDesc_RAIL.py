for item in context.AffectedItems:
    query = "select Material, SalesOrg,DC,SalesText,CpqTableEntryId from LBF_QU_SALESORG_INFO where Material = '{0}' and SalesOrg = '{1}' and DC = '{2}'".format(item.PartNumber, item["LBF_QU_SalesOrg"],item["LBF_QU_DC"])
    res = SqlHelper.GetFirst(query)
    if item['LBF_QU_Notes']:
        pass
    else:
        Log.Info("LBF_QU_LongDesc_RAIL@@---->"+str(res.SalesText))
        item['LBF_QU_Notes'] = res.SalesText