class FMTOTCOST():
    def __init__(self):
        self.count = 0

    def conTbl(self,tbl):
        pumpCon = Product.GetContainerByName(tbl).Rows
        if pumpCon.Count > 0:
            for row in pumpCon:
                if row['Ext Cost']:
                    Trace.Write(row['Ext Cost'])
                    return float(row['Ext Cost'])
                else:
                    Trace.Write(row['Ext Cost'])
                    return 0
        else:
            return 0

    def totalCost(self):
        totCost = 0
        for tbl in ['LBF_AR_FM_1PUMP','LBF_AR_FM_2POWER','LBF_AR_FM_3SIZE','LBF_AR_FM_4BAR','LBF_AR_FM_5RLSZCL','LBF_AR_FM_7SPECIAL1','LBF_AR_FM_8SENSOR','LBF_AR_FM_9SPL2']:
            totCost = totCost+float(self.conTbl(tbl))
        Trace.Write(totCost)
        Product.Attr('LBF_AT_FM_TOTALCOST').AssignValue(str(totCost))
object = FMTOTCOST().totalCost()
Trace.Write(object)