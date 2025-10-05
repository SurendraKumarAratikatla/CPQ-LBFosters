class freight():
    def __init__(self):
        pass

    def freightCheck(self, item):
        if item['LBF_QU_FREIGHT'] == "QT":
            item['LBF_QU_FREIGHT_CST_EXT'] =  str(float(item["LBF_QU_FREIGHT_CST"]) * item.Quantity)
        elif item['LBF_QU_FREIGHT'] == "WT":
            sqlLineData = SqlHelper.GetFirst("select MATERIAL,GROSS_WEIGHT from LBF_QU_MAT_COST where MATERIAL = '{0}'".format(item.PartNumber))
            if sqlLineData:
                item['LBF_QU_FREIGHT_CST_EXT'] =  str(float(item["LBF_QU_FREIGHT_CST"]) * int(item.Quantity) * float(sqlLineData.GROSS_WEIGHT))
        elif item['LBF_QU_FREIGHT'] == "FC":
            item['LBF_QU_FREIGHT_CST_EXT'] = str(item["LBF_QU_FREIGHT_CST"])

    def freighCost(self):
        for item in context.AffectedItems:
            if not item['LBF_QU_MAT_CST_OVR']:
                if item['LBF_QU_FREIGHT'] and item['LBF_QU_FREIGHT_CST'] and item.Quantity:
                    self.freightCheck(item)
                else:
                    item['LBF_QU_FREIGHT_CST_EXT'] = "0.00"
            else:
                self.freightCheck(item)

    def run(self):
        self.freighCost()


object = freight().run()