distance = Product.Attr('Distance').SelectedValue.UserInput
if distance == "500" or distance == "1000" or distance == "2000":
    components_con = Product.GetContainerByName('Components').Rows
    totalCost = 0
    totalHighPrice = 0
    totalMediumPrice = 0
    totalLowPrice = 0
    for row in components_con:
        conComponent = row['Component']
        if conComponent == 'CCTV':
            tableData = SqlHelper.GetFirst("select Component, cost, high, medium, low from LBF_ROCKFALL where Component='{0}'".format(conComponent))
            Trace.Write(row['Component'])
            if tableData and row["Qty"] != "0":
                qty = int(row['Qty'])
                row['High'] = str(tableData.high * qty)
                row['Medium'] = str(tableData.medium * qty)
                row['Low'] = str(tableData.low * qty)
                row['Cost'] = str(tableData.cost * qty)
                totalCost = int(totalCost) + int(row['Cost'])
                totalHighPrice = int(totalHighPrice) + int(row['High'])
                totalMediumPrice = int(totalMediumPrice) + int(row['Medium'])
                totalLowPrice = int(totalLowPrice) + int(row['Low'])
        elif conComponent == 'Lidar' or conComponent == 'Men' or conComponent == 'Control panel':
            tableData = SqlHelper.GetFirst("select RFQTY.Component AS Component, RFQTY.Distance AS Distance, RFQTY.Qty AS Qty, RF.cost AS cost, RF.high AS high, RF.medium AS medium, RF.low AS low, RF.Product AS Product from LBF_ROCKFALL_QTY AS RFQTY JOIN LBF_ROCKFALL AS RF ON RFQTY.Component = RF.Component where Distance = '{0}' and RFQTY.Component = '{1}'".format(distance,conComponent))
            Trace.Write(row['Component'])
            if tableData:
                qty = int(row['Qty'])
                row['High'] = str(tableData.high * qty)
                row['Medium'] = str(tableData.medium * qty)
                row['Low'] = str(tableData.low * qty)
                row['Cost'] = str(tableData.cost * qty)
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
