#def fm_applicator_brackets():
con = Product.GetContainerByName('FM AppsBrackets Selection Container')
con.Clear()
selected_values_str = Product.Attr('LBF_AR_FM_ProductType').GetValue()

if selected_values_str:
    selected_values = [val.strip() for val in selected_values_str.split(",")]
    formatted_values = ",".join("'" + val + "'" for val in selected_values)
    selected_site = Product.Attr('LBF_AR_Site').GetValue()
    query = "SELECT * FROM LBF_QU_FM_PRODUCTS WHERE ProductType IN (" + formatted_values + ")"
    if selected_site:
        query += " AND SiteID = '" + selected_site + "'"
    data_rows = SqlHelper.GetList(query)
    #currency exchange rate
    req_currency = Product.Attr('LBF_AR_Currency').GetValue()
    query_currencies = SqlHelper.GetFirst("Select CURRENCY, QUOTE from CURRENCIES WHERE CURRENCY ='{0}'".format(req_currency))
    for data in data_rows:
        rowData = {
            'PN': str(data.PartNumber),
            'Description': str(data.Description),
            'Cost_of_20': str(float(data.Cost)*float(query_currencies.QUOTE)),
            'Qty': "1",
            'Cost_CAD': str(data.Cost),
            'Site': str(data.SiteID),
            'IntercoMarkup': "0",
            'QuoteUnitCostCAD': str(data.Cost),
            'ConverttoUSD': "1",
            'QuoteUnitCostUSD': str(data.Cost),
            'Product_Type': str(data.ProductType)
        }

        newRow = con.AddNewRow(False)
        for key, val in rowData.items():
            newRow[key] = val

#fm_applicator_brackets()