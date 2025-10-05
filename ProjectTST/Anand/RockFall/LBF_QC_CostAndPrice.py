#for item in context.Quote.GetAllItems():
for item in context.AffectedItems:
    ProductSystemId = item.ProductSystemId
    partnumber = item.PartNumber
    ProductTypeName = item.ProductTypeName
    if partnumber == "RFMS":
        for attr in item.SelectedAttributes:
            if attr.Name == 'LBF_AR_RFS_TEMPLISTPRICE':
                item["LBF_QU_PRICE"] = attr.Values[0].Display
            if attr.Name == 'LBF_AR_RFS_TEMPCOST':
                item["LBF_QU_COST"] = attr.Values[0].Display