for item in context.AffectedItems():
    ProductSystemId = item.ProductSystemId
    partnumber = item.PartNumber
    ProductTypeName = item.ProductTypeName
    if partnumber == "ROCKFALL":
        for attr in item.SelectedAttributes:
            if attr.Name == 'Temp_ListPrice':
                item["LBF_Price"] = attr.Values[0].Display
            if attr.Name == 'Temp_Cost':
                item["LBF_Cost"] = attr.Values[0].Display