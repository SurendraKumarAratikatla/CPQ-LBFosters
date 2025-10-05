def accessMatCostTbl(prtNo):
    # prtNo = self.Product.PartNumber
    data = SqlHelper.GetFirst("SELECT * from LBF_QU_MAT_COST WHERE MATERIAL = '{0}' ".format(prtNo))
    if data:
        # if str(self.marketId) != "8" and str(self.marketId) != "7":
        try:
            currentPlant = Product.Attr('Plant (Own or External)').GetValue()
            Trace.Write("currentPlant000:--->"+str(currentPlant))

        except Exception as e:
            currentPlant = data.Plant
            Log.Info('Error Ignore: Plant (Own or External) :'+str(e))
            Trace.Write("currentPlant111:--->"+str(currentPlant))

        Trace.Write("currentPlant:--->"+str(currentPlant))
        plant = str(currentPlant)
        salesOrg = data.SORG
        disCha = data.DC
        division = data.DIV
accessMatCostTbl("HH_NEW_T_RAIL")