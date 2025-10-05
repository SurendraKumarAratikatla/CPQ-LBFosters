components_con = Product.GetContainerByName('Components').Rows
totalCost = Product.ParseString('<*CTX( Container(Components).Sum(Cost) )*>')
totalHigh =Product.ParseString(' <*CTX( Container(Components).Sum(High) )*>')
totalMedium = Product.ParseString('<*CTX( Container(Components).Sum(Medium) )*>')
totalLow = Product.ParseString('<*CTX( Container(Components).Sum(Low) )*>')
totalCost = Product.ParseString('<*CTX( Container(Components).Sum(Cost) )*>')
totalHighPrice =Product.ParseString(' <*CTX( Container(Components).Sum(High) )*>')
totalMediumPrice = Product.ParseString('<*CTX( Container(Components).Sum(Medium) )*>')
totalLowPrice = Product.ParseString('<*CTX( Container(Components).Sum(Low) )*>')
GPForHigh = (float(int(totalHighPrice) - int(totalCost))/float(totalHighPrice)) * 100  #GP = ((Total price - Total Cost)/Total Price) * 100
GPForMedium = (float(int(totalMediumPrice) - int(totalCost))/float(totalMediumPrice)) * 100
GPForLow = (float(int(totalLowPrice) - int(totalCost))/float(totalLowPrice)) * 100
for row in components_con:
    conComponent = row['Component']
    if conComponent == 'CCTV':
        tableData = SqlHelper.GetFirst("select Component, cost, high, medium, low from LBF_ROCKFALL where Component='{0}'".format(conComponent))
        Trace.Write(row['Component'])
        if tableData:
            qty = int(row['Qty'])
            row['High'] = str(tableData.high * qty)
            row['Medium'] = str(tableData.medium * qty)
            row['Low'] = str(tableData.low * qty)
            row['Cost'] = str(tableData.cost * qty)

    elif conComponent == "Total":
        row["Cost"] = str(totalCost)
        row["High"] = str(totalHigh)
        row["Medium"] = str(totalMedium)
        row["Low"] = str(totalLow)

    elif conComponent == "GP":
        row["High"] = str(GPForHigh)
        row["Medium"] = str(GPForMedium)
        row["Low"] = str(GPForLow)
