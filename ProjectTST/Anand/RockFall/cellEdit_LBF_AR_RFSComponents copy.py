distance = Product.Attr('LBF_AR_RFSDist').SelectedValue.UserInput
components_con = Product.GetContainerByName('LBF_AR_RFSComponents').Rows
totalCost = 0
totalHighPrice = 0
totalMediumPrice = 0
totalLowPrice = 0
flag = "False"
tempPrevQty = Product.Attr('LBF_AR_RFS_TEMPCOST').GetValue()
for row in components_con:
    conComponent = row['Component']
    #if str(tempPrevQty) != str(row["Qty"]):
    if conComponent == 'CCTV':
        tableData = SqlHelper.GetFirst("select Component, cost, high, medium, low from LBF_QU_RFS where Component='{0}'".format(conComponent))
        Trace.Write(row['Component'])
        # if tableData and row["Qty"] != "0":
        try:
            if tableData:
                if str(row["Qty"]) != "0" and int(row["Qty"]) > 0:
                    qty = int(row['Qty'])
                    row['High'] = str(tableData.high * qty)
                    row['Medium'] = str(tableData.medium * qty)
                    row['Low'] = str(tableData.low * qty)
                    row['Cost'] = str(tableData.cost * qty)
                    totalCost = int(totalCost) + int(row['Cost'])
                    totalHighPrice = int(totalHighPrice) + int(row['High'])
                    totalMediumPrice = int(totalMediumPrice) + int(row['Medium'])
                    totalLowPrice = int(totalLowPrice) + int(row['Low'])
                    if str(tempPrevQty) != str(row["Qty"]):
                        revTempAttr = Product.Attr('LBF_AR_RFSDist').AssignValue(str(row['Qty']))
                        flag = "True"
                    else:
                        flag = "False"
                        pass
                else:
                    row['Qty'] = "0"
                    qty = int(row['Qty'])
                    row['High'] = str(tableData.high * qty)
                    row['Medium'] = str(tableData.medium * qty)
                    row['Low'] = str(tableData.low * qty)
                    row['Cost'] = str(tableData.cost * qty)
                    totalCost = int(totalCost) + int(row['Cost'])
                    totalHighPrice = int(totalHighPrice) + int(row['High'])
                    totalMediumPrice = int(totalMediumPrice) + int(row['Medium'])
                    totalLowPrice = int(totalLowPrice) + int(row['Low'])
        except:
            pass
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

    elif conComponent == "Total" and flag == "False":
        GPForHigh = (float(float(totalHighPrice) - float(totalCost))/float(totalHighPrice)) * 100  #GP = ((Total price - Total Cost)/Total Price) * 100
        GPForMedium = (float(float(totalMediumPrice) - float(totalCost))/float(totalMediumPrice)) * 100
        GPForLow = (float(float(totalLowPrice) - float(totalCost))/float(totalLowPrice)) * 100
    
    elif conComponent == "Total" and flag == "True":
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
