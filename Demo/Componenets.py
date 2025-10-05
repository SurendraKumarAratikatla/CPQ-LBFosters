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