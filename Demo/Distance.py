distance = Product.Attr('Distance').SelectedValue.UserInput
components_con = Product.GetContainerByName('Components').Rows

for row in components_con:
    conComponent = row['Component']
    if conComponent != 'CCTV':
        tableData = SqlHelper.GetFirst("select RFQTY.Component AS Component, RFQTY.Distance AS Distance, RFQTY.Qty AS Qty, RF.cost AS cost, RF.high AS high, RF.medium AS medium, RF.low AS low, RF.Product AS Product from LBF_ROCKFALL_QTY AS RFQTY JOIN LBF_ROCKFALL AS RF ON RFQTY.Component = RF.Component where Distance = '{0}' and RFQTY.Component = '{1}'".format(distance,conComponent))
        Trace.Write(row['Component'])
        if tableData:
            row['Qty'] = str(tableData.Qty)
            row['High'] = str(tableData.high * tableData.Qty)
            row['Medium'] = str(tableData.medium * tableData.Qty)
            row['Low'] = str(tableData.low * tableData.Qty)
            row['Cost'] = str(tableData.cost * tableData.Qty)
            Log.Info("------------------------------------------>")
totalCost = Product.ParseString('<*CTX( Container(Components).Sum(Cost) )*>')
totalHigh =Product.ParseString(' <*CTX( Container(Components).Sum(High) )*>')
totalMedium = Product.ParseString('<*CTX( Container(Components).Sum(Medium) )*>')
totalLow = Product.ParseString('<*CTX( Container(Components).Sum(Low) )*>')
totalHighPrice =Product.ParseString(' <*CTX( Container(Components).Sum(High) )*>')
totalMediumPrice = Product.ParseString('<*CTX( Container(Components).Sum(Medium) )*>')
totalLowPrice = Product.ParseString('<*CTX( Container(Components).Sum(Low) )*>')
GPForHigh = (float(float(totalHighPrice) - float(totalCost))/float(totalHighPrice)) * 100  #GP = ((Total price - Total Cost)/Total Price) * 100
GPForMedium = (float(float(totalMediumPrice) - float(totalCost))/float(totalMediumPrice)) * 100
GPForLow = (float(float(totalLowPrice) - float(totalCost))/float(totalLowPrice)) * 100
for row in components_con:
    if row["Component"] == "Total":
        row["Cost"] = str(totalCost)
        row["High"] = str(totalHigh)
        row["Medium"] = str(totalMedium)
        row["Low"] = str(totalLow)
    elif row["Component"] == "GP":
        row["High"] = str(GPForHigh)
        row["Medium"] = str(GPForMedium)
        row["Low"] = str(GPForLow)
