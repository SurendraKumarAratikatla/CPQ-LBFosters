import math
class Distance():
    def __init__(self):
        self.distance = Product.Attr('LBF_AR_RFSDist').SelectedValue.UserInput
        self.components_con = Product.GetContainerByName('LBF_AR_RFSComponents').Rows

    def RFMSDistance(self):
        lidarQty = 0
        menQty = 0
        totalCost = 0
        totalHighPrice = 0
        totalMediumPrice = 0
        totalLowPrice = 0
        for row in self.components_con:
            conComponent = row['Component']
            if conComponent == 'LiDAR' or conComponent == 'MEN' or conComponent == 'Control Panel' or conComponent == 'Fibre Converter':
                tableData = SqlHelper.GetFirst("select Component, cost, high, medium, low, Qty from LBF_QU_RFS where Component='{0}'".format(conComponent))
                if tableData:
                    if conComponent == "LiDAR":
                        row['Qty'] = str(math.ceil(float(float(self.distance) / float(tableData.Qty)) + 1))
                        lidarQty = row['Qty']
                    elif conComponent == "MEN":
                        Trace.Write('lidarQty-->'+str(lidarQty))
                        row['Qty'] = str(math.ceil(float(lidarQty) / float(tableData.Qty)))
                        menQty = row['Qty']
                    elif conComponent == "Control Panel":
                        Trace.Write('menQty-->'+str(menQty))
                        row['Qty'] = str(math.ceil(float(menQty) / float(tableData.Qty)))
                    elif conComponent == "Fibre Converter":
                        row['Qty'] = str(tableData.Qty)
                        row['Cost'] = str(tableData.cost)

                    Qty = int(row['Qty'].split('.')[0])
                    Trace.Write(Qty)
                    row['High'] = str(int(tableData.high) * Qty)
                    row['Medium'] = str(int(tableData.medium) * Qty)
                    row['Low'] = str(int(tableData.low) * Qty)
                    row['Cost'] = str(int(tableData.cost) * Qty)
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

    def run(self):
        self.RFMSDistance()


object = Distance().run()
