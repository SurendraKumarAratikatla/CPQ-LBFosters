distance = Product.Attr('LBF_AR_RFSDist').SelectedValue.UserInput
components_con = Product.GetContainerByName('LBF_AR_RFSComponents').Rows
totalCost = 0
totalHighPrice = 0
totalMediumPrice = 0
totalLowPrice = 0

for row in components_con:
    conComponent = row['Component']
    Trace.Write("out---"+str(row['Component']))
    if conComponent == 'LiDAR' or conComponent == 'MEN' or conComponent == 'Control Panel':
        tableData = SqlHelper.GetFirst("select Component, cost, high, medium, low, Qty from LBF_QU_RFS where Component='{1}'".format(distance,conComponent))
        Trace.Write(row['Component'])
        if tableData:
            row['Qty'] = str(tableData.Qty)
            Qty = int(tableData.Qty)
            #row['High'] = str(tableData.high * tableData.Qty)
            row['High'] = str(tableData.high * Qty)
            row['Medium'] = str(tableData.medium * Qty)
            #row['Low'] = str(tableData.low * tableData.Qty)
            row['Low'] = str(tableData.low * Qty)
            #row['Cost'] = str(tableData.cost * tableData.Qty)
            row['Cost'] = str(tableData.cost * Qty)
            Trace.Write(row.RowIndex)
            totalCost = int(totalCost) + int(row['Cost'])
            totalHighPrice = int(totalHighPrice) + int(row['High'])
            totalMediumPrice = int(totalMediumPrice) + int(row['Medium'])
            totalLowPrice = int(totalLowPrice) + int(row['Low'])
    elif conComponent == "Total":
        row["Cost"] = str(totalCost)
        row["High"] = str(totalHighPrice)
        row["Medium"] = str(totalMediumPrice)
        row["Low"] = str(totalLowPrice)
        GPForHigh = (float(float(totalHighPrice) - float(totalCost))/float(totalHighPrice)) * 100  #GP = ((Total price - Total Cost)/Total Price) * 100
        GPForMedium = (float(float(totalMediumPrice) - float(totalCost))/float(totalMediumPrice)) * 100
        GPForLow = (float(float(totalLowPrice) - float(totalCost))/float(totalLowPrice)) * 100
    elif conComponent == "GP":
        row["High"] = str(GPForHigh)
        row["Medium"] = str(GPForMedium)
        row["Low"] = str(GPForLow)