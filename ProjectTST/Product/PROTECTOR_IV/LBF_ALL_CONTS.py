class Size():
    def __init__(self):
        self.count = 0

    def conTbl(self,tbl):
        pumpCon = Product.GetContainerByName(tbl).Rows
        for row in pumpCon:
            if row['Code']:
                self.count = self.count + 1
                return row['Code']
            else:
                return ' '
            
    def createUpdatePartNumber(self,cusPartNumber):
        Product.Attr('LBF_AR_FM_PARTNUMBER').AssignValue(str(cusPartNumber))
        

    def updateUOM(self,flag):
        totCost = Product.Attr('LBF_AT_FM_TOTALCOST').GetValue() if flag else 0
        for row in context.Quote.GetAllItems():
            if str(row.RolledUpQuoteItem) == str(Product.ParseString('<*CTX( Quote.CurrentItem.RolledUpItemNumber )*>')):
                row['LBF_QU_FM_COST'] = str(totCost)
                break


    def railSize(self):
        cusPartNumber = "74"
        for tbl in ['LBF_AR_FM_1PUMP','LBF_AR_FM_2POWER','LBF_AR_FM_3SIZE','LBF_AR_FM_4BAR','LBF_AR_FM_5RLSZCL','LBF_AR_FM_7SPECIAL1','LBF_AR_FM_8SENSOR','LBF_AR_FM_9SPL2']:
            cusPartNumber = cusPartNumber+str(self.conTbl(tbl))
        Trace.Write(self.count)
        Trace.Write(cusPartNumber)
        if self.count == 8:
            self.createUpdatePartNumber(cusPartNumber)
            self.updateUOM(True)
        else:
            self.createUpdatePartNumber('')
            self.updateUOM(False)

object = Size().railSize()



for row in context.Quote.GetAllItems():
    Trace.Write(row.SelectedAttributes)
    for attr in row.SelectedAttributes:
        if attr.Name == "LBF_AT_FM_TOTALCOST":
            for val in attr.Values:
                Trace.Write(val.Display)