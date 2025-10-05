class freight():
    def __init__(self):
        pass

    def freightCheck(self, item):
        if item['LBF_QU_FREIGHT'] == "QT":
            Trace.Write("111111111111111111")
            item['LBF_QU_FREIGHT_CST_EXT'] =  str(float(item["LBF_QU_FREIGHT_CST"]) * item.Quantity)
        elif item['LBF_QU_FREIGHT'] == "WT":
            sqlLineData = SqlHelper.GetFirst("select MATERIAL,GROSS_WEIGHT from LBF_QU_MAT_COST where MATERIAL = '{0}'".format(item.PartNumber))
            if sqlLineData and int(float(sqlLineData.GROSS_WEIGHT)) != 0:
                Trace.Write("222222222222222222")
                item['LBF_QU_FREIGHT_CST_EXT'] =  str(float(item["LBF_QU_FREIGHT_CST"]) * float(item.Quantity) * float(sqlLineData.GROSS_WEIGHT))
            elif item.PartNumber == "SS_NEW_T_RAIL2":
                wt = None
                config =JsonHelper.Deserialize(item.ExternalConfiguration)
                conf_id = config["rootItem"]["characteristics"]
                for conf in conf_id:
                    if conf["id"] == "SD_G_WT":
                        wt = conf["values"][0]["value"]
                        Trace.Write("--------------")
                Trace.Write("3333333333333333333333333")
                item['LBF_QU_FREIGHT_CST_EXT'] =  str(float(item["LBF_QU_FREIGHT_CST"]) * float(item.Quantity) * float(wt))
        elif item['LBF_QU_FREIGHT'] == "FC":
            Trace.Write("44444444444444444444444")
            item['LBF_QU_FREIGHT_CST_EXT'] = str(item["LBF_QU_FREIGHT_CST"])

    def freighCost(self):
        for item in context.AffectedItems:
            if not item['LBF_QU_MAT_CST_OVR']:
                if item['LBF_QU_FREIGHT'] and item['LBF_QU_FREIGHT_CST'] and item.Quantity:
                    self.freightCheck(item)
                else:
                    Trace.Write("555555555555555")
                    item['LBF_QU_FREIGHT_CST_EXT'] = "0.00"
            else:
                self.freightCheck(item)

    def run(self):
        self.freighCost()


object = freight().run()