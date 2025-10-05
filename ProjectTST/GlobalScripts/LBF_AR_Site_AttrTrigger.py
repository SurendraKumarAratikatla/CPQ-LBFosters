# Always clear the container first
Product.GetContainerByName('FM AppsBrackets Selection Container').Clear()

# Get selected Site
selected_site = Product.Attr('LBF_AR_Site').GetValue()

# Assign currency based on site selection
if selected_site == "VAN":
    Product.Attr("LBF_AR_Currency").SelectValue("CAD")
elif selected_site == "RMP":
    Product.Attr("LBF_AR_Currency").SelectValue("USD")
else:
    Product.Attr("LBF_AR_Currency").SelectValue("")

# Get selected Product Types (can be empty)
selected_values_str = Product.Attr('LBF_AR_FM_ProductType').GetValue()

# Only proceed if product types are selected
if selected_values_str:
    selected_values = selected_values_str.split(",")  # Convert string to list
    formatted_values = ",".join(["'" + val.strip() + "'" for val in selected_values])

    # Build SQL query
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
        newRow['Product_Type'] = str(data.ProductType)
