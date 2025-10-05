'''Product.GetContainerByName('FM AppsBrackets Selection Container').Clear()

selected_values_str = Product.Attr('LBF_AR_FM_ProductType').GetValue ()

if selected_values_str:
    selected_values = selected_values_str.split(",")  # Convert string to list
    formatted_values = ",".join(["'" + val.strip() + "'" for val in selected_values])

    query = "SELECT * FROM LBF_QU_FM_PRODUCTS WHERE ProductType IN (" + formatted_values + ")"
    data_rows = SqlHelper.GetList(query)

    con = Product.GetContainerByName('FM AppsBrackets Selection Container')

    for data in data_rows:
        newRow = con.AddNewRow(True)
        newRow['PN'] = str(data.PartNumber)
        #newRow.Product.Attr('LBF_AR_WILDH4').AssignValue(str(data['PN']))
        newRow['Description'] = str(data.Description)
        #newRow.Product.Attr('LBF_AR_WILDH1').AssignValue(str(data['Description']))
        newRow['Cost_of_20'] = str(data.Cost)
        #newRow.Product.Attr('LBF_AR_WILDH3').AssignValue(str(data['Cost']))
        newRow['Qty'] = "1"
        newRow['Cost_CAD'] = str(data.Cost)
        newRow['Site'] = ""
        newRow['IntercoMarkup'] = "0"
        newRow['QuoteUnitCostCAD'] = str(data.Cost)
        newRow['ConverttoUSD'] = "1"
        newRow['QuoteUnitCostUSD'] = str(data.Cost)
        newRow['Product_Type'] = str(data.ProductType)
        newRow['Site'] = str(data.SiteID)'''


'''Product.GetContainerByName('FM AppsBrackets Selection Container').Clear()

selected_values_str = Product.Attr('LBF_AR_FM_ProductType').GetValue()

if selected_values_str:
    selected_values = selected_values_str.split(",")  # Convert string to list
    formatted_values = ",".join(["'" + val.strip() + "'" for val in selected_values])

    # Get selected Site
    selected_site = Product.Attr('LBF_AR_Site').GetValue()

    # Build SQL query with optional Site filter
    query = "SELECT * FROM LBF_QU_FM_PRODUCTS WHERE ProductType IN (" + formatted_values + ")"
    if selected_site:
        query += " AND SiteID = '" + selected_site + "'"

    data_rows = SqlHelper.GetList(query)

    con = Product.GetContainerByName('FM AppsBrackets Selection Container')

    for data in data_rows:
        newRow = con.AddNewRow(True)
        newRow['PN'] = str(data.PartNumber)
        newRow['Description'] = str(data.Description)
        newRow['Cost_of_20'] = str(data.Cost)
        newRow['Qty'] = "1"
        newRow['Cost_CAD'] = str(data.Cost)
        newRow['Site'] = str(data.SiteID)
        newRow['IntercoMarkup'] = "0"
        newRow['QuoteUnitCostCAD'] = str(data.Cost)
        newRow['ConverttoUSD'] = "1"
        newRow['QuoteUnitCostUSD'] = str(data.Cost)
        newRow['Product_Type'] = str(data.ProductType)'''

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

    for data in data_rows:
        rowData = {
            'PN': str(data.PartNumber),
            'Description': str(data.Description),
            'Cost_of_20': str(data.Cost),
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

