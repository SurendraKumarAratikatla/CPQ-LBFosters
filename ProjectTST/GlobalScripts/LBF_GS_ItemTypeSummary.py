def ItemTypeSummary():
    quote_table = context.Quote.QuoteTables["ItemType_Summary"]
    quote_table.Rows.Clear()
    itemTypeList = []

    item_type_map = {}

    for item in context.Quote.GetAllItems():
        # product_type = item.ProductTypeName
        itemTypeOpt = item.AsMainItem.IsOptional
        itemTypeAlt = item.AsMainItem.IsAlternative
        itemTypeVar = item.AsMainItem.IsVariant
        if itemTypeOpt == True:
            item_type = "Optional"
            if item_type not in itemTypeList:
                itemTypeList.append(item_type) # ['Optional','Alternative'] # ['Optional'] #  ['Alternative']
        elif itemTypeAlt == True:
            item_type = "Alternative"
            if item_type not in itemTypeList:
                itemTypeList.append(item_type) # ['Optional','Alternative']
        elif itemTypeVar == True:
            item_type = "Variant"
        else:
            item_type = "Base"

        gp_val = float(item["LBF_QU_GP_VAL"] or 0.0)
        gp_per = float(item["LBF_QU_GP_PER"] or 0.0)
        Tot_Cst = float(item["LBF_QU_TOTAL_COST"] or 0.0)
        Tot_Sp = float(item["LBF_QU_SELPRICE"] or 0.0)

        if item_type not in item_type_map:
            item_type_map[item_type] = {
                "Gross_Profit_Margin_": 0.0,
                "Gross_Profit_": 0.0,
                "Total_Cost":0.0,
                "Total_Price":0.0,
                "count": 0
            }

        item_type_map[item_type]["Gross_Profit_Margin_"] += gp_val
        item_type_map[item_type]["Gross_Profit_"] += gp_per
        item_type_map[item_type]["Total_Cost"] += Tot_Cst
        item_type_map[item_type]["Total_Price"] += Tot_Sp
        item_type_map[item_type]["count"] += 1

    for itype, values in item_type_map.items():
        row = quote_table.AddNewRow()
        row["ItemType"] = itype
        row["Gross_Profit_Margin_"] = round(values["Gross_Profit_Margin_"], 2)
        row["Total_Cost"] = round(values["Total_Cost"], 2)
        row["Total_Price"] = round(values["Total_Price"], 2)
        if values["count"] > 0:
            row["Gross_Profit_"] = round(values["Gross_Profit_"] / values["count"], 2)
        else:
            row["Gross_Profit_"] = 0.0
        
        #Itemtype flag for document generation values
        if itype == "Optional":
            context.Quote.GetCustomField("LBF_CF_Itemtype_Optional").Value = row["Total_Price"]
        elif itype == "Alternative":
            context.Quote.GetCustomField("LBF_CF_Itemtype_Alternative").Value = row["Total_Price"] 


    if itemTypeList:
        if "Optional" in itemTypeList and "Alternative" in itemTypeList:
            context.Quote.GetCustomField("LBF_CF_Itemtype_Optional").Value = 'optional'
            context.Quote.GetCustomField("LBF_CF_Itemtype_Alternative").Value = 'alternative'
        elif "Optional" in itemTypeList:
            context.Quote.GetCustomField("LBF_CF_Itemtype_Optional").Value = 'optional'
            context.Quote.GetCustomField("LBF_CF_Itemtype_Alternative").Value = ''
        elif "Alternative" in itemTypeList:
            context.Quote.GetCustomField("LBF_CF_Itemtype_Optional").Value = ''
            context.Quote.GetCustomField("LBF_CF_Itemtype_Alternative").Value = 'alternative'
    else:
        context.Quote.GetCustomField("LBF_CF_Itemtype_Optional").Value = ''
        context.Quote.GetCustomField("LBF_CF_Itemtype_Alternative").Value = ''


ItemTypeSummary()
