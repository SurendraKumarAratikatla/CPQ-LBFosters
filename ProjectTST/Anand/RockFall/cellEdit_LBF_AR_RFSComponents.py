class Components():
    def __init__(self):
        self.totalCost = 0
        self.totalHighPrice = 0
        self.totalMediumPrice = 0
        self.totalLowPrice = 0
        self.flag = "False"
        
        self.distance = Product.Attr('LBF_AR_RFSDist').SelectedValue.UserInput
        self.components_con = Product.GetContainerByName('LBF_AR_RFSComponents').Rows
        self.prevTempAttrList = Product.Attr('LBF_AR_Temp_Qty').GetValue()
        self.currTempAttrList = []

    def listOfQtyComponent(self):
        for row in self.components_con:
            conComponent = row['Component']
            if conComponent == 'CCTV' or conComponent == 'LiDAR' or conComponent == 'MEN' or conComponent == 'Control Panel':
                self.currTempAttrList.append(row['Qty'].split('.')[0])

    def RFMSComponents(self):
        TempAttrList = []
        self.listOfQtyComponent()
        self.prevTempAttrList = JsonHelper.Deserialize(self.prevTempAttrList)
        Trace.Write(str(self.prevTempAttrList))
        Trace.Write(str(self.currTempAttrList))
        if self.prevTempAttrList != self.currTempAttrList:
            for row in self.components_con:
                conComponent = row['Component']
                if conComponent == 'CCTV' or conComponent == 'LiDAR' or conComponent == 'MEN' or conComponent == 'Control Panel':
                    tableData = SqlHelper.GetFirst("select Component, cost, high, medium, low from LBF_QU_RFS where Component='{0}'".format(conComponent))
                    Trace.Write(row['Component'])
                    #try:
                    if tableData:
                        try:
                            qty = int(row['Qty'].split('.')[0])
                        except:
                            qty = 0
                    
                        row['High'] = str(tableData.high * qty)
                        row['Medium'] = str(tableData.medium * qty)
                        row['Low'] = str(tableData.low * qty)
                        row['Cost'] = str(tableData.cost * qty)
                        self.totalCost = int(self.totalCost) + int(row['Cost'])
                        self.totalHighPrice = int(self.totalHighPrice) + int(row['High'])
                        self.totalMediumPrice = int(self.totalMediumPrice) + int(row['Medium'])
                        self.totalLowPrice = int(self.totalLowPrice) + int(row['Low'])
                        TempAttrList.append(str(qty))

                
                elif conComponent == "Total":
                    row["Cost"] = str(self.totalCost)
                    row["High"] = str(self.totalHighPrice)
                    row["Medium"] = str(self.totalMediumPrice)
                    row["Low"] = str(self.totalLowPrice)
                    GPForHigh = (float(float(self.totalHighPrice) - float(self.totalCost))/float(self.totalHighPrice)) * 100  #GP = ((Total price - Total Cost)/Total Price) * 100
                    GPForMedium = (float(float(self.totalMediumPrice) - float(self.totalCost))/float(self.totalMediumPrice)) * 100
                    GPForLow = (float(float(self.totalLowPrice) - float(self.totalCost))/float(self.totalLowPrice)) * 100

                elif conComponent == "GP":
                    row["High"] = str(GPForHigh)
                    row["Medium"] = str(GPForMedium)
                    row["Low"] = str(GPForLow)
            Product.Attr('LBF_AR_Temp_Qty').AssignValue(str(TempAttrList))
            Trace.Write("endddd..............")

    def run(self):
        self.RFMSComponents()


object = Components().run()
