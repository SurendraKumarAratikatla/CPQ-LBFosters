def update_Notes():
    for item in context.Quote.GetAllItems():
        # updating the Additional Item Notes (LBF_QU_Notes)
        if item['LBF_QU_SalesOrg'] == "2100" or item['LBF_QU_SalesOrg'] == "1000": # transit(2100) and rail(1000), we can extend this going forward for other models
            #query_template = "select Notes, Material from LBF_QU_TR_MATERIALS where Material = '{0}'".format(item.PartNumber)
            query_template = "select Material, SalesOrg,DC,SalesText,CpqTableEntryId from LBF_QU_SALESORG_INFO where Material = '{0}' and SalesOrg = '{1}' and DC = '{2}'".format(item.PartNumber, item["LBF_QU_SalesOrg"],item["LBF_QU_DC"])
            result = SqlHelper.GetFirst(query_template)
            if result:
                if item['LBF_QU_Notes']:
                    pass
                else:
                    #Log.Info('result is Notes ->' + result.SalesText)
                    lines = [line.strip() for line in str(result.SalesText).split('|') if line.strip()]
                    multi_line_str = '\n'.join(lines)
                    item['LBF_QU_Notes'] = multi_line_str


        # updaing the Item Description (LBF_QU_ITEMDESC)
        if item['LBF_QU_ITEMDESC']:
            pass
        else:
            item['LBF_QU_ITEMDESC'] = item.Description



update_Notes()