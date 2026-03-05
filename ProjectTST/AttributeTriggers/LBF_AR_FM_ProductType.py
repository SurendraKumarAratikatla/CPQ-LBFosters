def fm_applicator_brackets():
    con = Product.GetContainerByName('FM AppsBrackets Selection Container')
    con.Clear()
    selected_values_str = Product.Attr('LBF_AR_FM_ProductType').GetValue()

    if selected_values_str:
        selected_values = [val.strip() for val in selected_values_str.split(",")]
        # formatted_values = ",".join("'" + val + "'" for val in selected_values)
        # Build SQL query
        if len(selected_values) == 2:
            query = "select * from LBF_QU_INFOR_MAT_COST where PARTNUMBER LIKE 'RB%' OR PARTNUMBER LIKE 'RA%'"

        else:
            fm = ''
            if "Applicators" in selected_values:
                fm = "RA"
            elif "Brackets" in selected_values:
                fm = "RB"
            query = "select * from LBF_QU_INFOR_MAT_COST where PARTNUMBER LIKE '{0}%'".format(fm)

        selected_site = Product.Attr('LBF_AR_Site').GetValue()
        # query = "SELECT * FROM LBF_QU_FM_PRODUCTS WHERE ProductType IN (" + formatted_values + ")"
        if selected_site:
            query += " AND SiteID = '" + selected_site + "'"
        data_rows = SqlHelper.GetList(query)
        #currency exchange rate
        req_currency = Product.Attr('LBF_AR_Currency').GetValue()
        query_currencies = SqlHelper.GetFirst("Select CURRENCY, QUOTE from CURRENCIES WHERE CURRENCY ='{0}'".format(req_currency))
        for data in data_rows:
            if "RA" in str(data.PARTNUMBER):
                pro_type = "Applicators"
                qtyData = SqlHelper.GetFirst("Select PoweCurveCostRatio, Qty from LBF_QU_FM_PCR_RA WHERE Qty ='{0}'".format("1"))
            elif "RB" in str(data.PARTNUMBER):
                pro_type = "Brackets"
                qtyData = SqlHelper.GetFirst("Select PoweCurveCostRatio, Qty from LBF_QU_FM_PCR_RB WHERE Qty ='{0}'".format("1"))
            else:
                pro_type = ""
                qtyData = ""
            
            if qtyData:
                unitCostUSD = str(float(float(data.UNIT_COST_USD)*float(query_currencies.QUOTE)) * float(qtyData.PoweCurveCostRatio))
            rowData = {
                'PN': str(data.PARTNUMBER),
                'Description': str(data.DESCRIPTION),
                'Cost_of_20': str(float(data.UNIT_COST_USD)*float(query_currencies.QUOTE)),
                'Qty': "1",
                'Cost_CAD': str(unitCostUSD),
                'Site': str(data.SITEID),
                'IntercoMarkup': "0",
                'QuoteUnitCostCAD': str(data.UNIT_COST_USD),
                'ConverttoUSD': "1",
                'QuoteUnitCostUSD': str(data.UNIT_COST_USD),
                'Product_Type': str(pro_type)
            }
            newRow = con.AddNewRow(False)
            for key, val in rowData.items():
                newRow[key] = val


fm_applicator_brackets()