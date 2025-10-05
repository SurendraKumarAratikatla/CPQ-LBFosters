class protectorCon():
    def __init__(self, conName):
        self.partNumber = Product.Attr('LBF_AR_FM_PARTNUMBER').GetValue()
        self.IVCon = Product.GetContainerByName(conName).Rows

    def conTbl(self,tbl):
        IVCon = Product.GetContainerByName(tbl).Rows
        if IVCon.Count > 0:
            for row in IVCon:
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
        for tbl in ['LBF_AR_FM_1PUMP','LBF_AR_FM_2POWER','LBF_AR_FM_3SIZE','LBF_AR_FM_4BAR','LBF_AR_FM_5RLSZCL','LBF_AR_FM_6BARQTY','LBF_AR_FM_7SPECIAL1','LBF_AR_FM_8SENSOR','LBF_AR_FM_9SPL2']:
            totCost = totCost+float(self.conTbl(tbl))
        Trace.Write(totCost)
        Product.Attr('LBF_AT_FM_TOTALCOST').AssignValue(str(totCost))
        
        
    def run(self,DBconName):
        for row in self.IVCon:
            Trace.Write(row['Code'])
            description = row['Description']
            sqlData = SqlHelper.GetFirst("select PARTNO,Code,Description from LBF_QU_FM_PROIV where PARTNO='{0}' and Code='{1}'".format(DBconName,description))
            Trace.Write(row['Description'])
            if sqlData:
                row['Code'] = str(sqlData.Code)
                Trace.Write("sqlData.Code----------------->"+str(sqlData.Code))
                if self.partNumber:
                    Trace.Write("row['Code']------------------>"+str(row['Code']))
                    row['Ext Cost'] = str(float(row['Cost']) * int(row['Qty']))
                    self.totalCost()

conName = 'LBF_AR_FM_1PUMP'
DBconName = 'PUMP'
object = protectorCon(conName).run(DBconName)
