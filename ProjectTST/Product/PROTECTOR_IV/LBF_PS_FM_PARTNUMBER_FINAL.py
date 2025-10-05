from Scripting.QuoteTables import AccessLevel

class Size():
    def __init__(self):
        self.count = 0

    def conTbl(self,tbl):
        if tbl == "LBF_AR_FM_6BARQTY":
            pumpCon = Product.GetContainerByName(tbl).Rows
            for row in pumpCon:
                if row['Qty']:
                    self.count = self.count + 1
                    return row['Qty']
                else:
                    return ''

        elif tbl == "LBF_AR_FM_9SPL2":
            pumpCon = Product.GetContainerByName(tbl).Rows
            for row in pumpCon:
                if row['Code'] == 'NONE':
                    self.count = self.count + 1
                    # if row['Qty'] or row['cell']:
                    for cell in pumpCon.Cells:
                        cell['Cost'] = AccessLevel.ReadOnly
                        cell['Qty'] = AccessLevel.ReadOnly
                    return 'NONE'
                elif row['Code']:
                    self.count = self.count + 1
                    return row['Code']
                else:
                    return ''        

        else:
            pumpCon = Product.GetContainerByName(tbl).Rows
            for row in pumpCon:
                if row['Code']:
                    self.count = self.count + 1
                    return row['Code']
                else:
                    return ''
            
    def createUpdatePartNumber(self,cusPartNumber):
        Product.Attr('LBF_AR_FM_PARTNUMBER').AssignValue(str(cusPartNumber))


    def railSize(self):
        cusPartNumber = "74"
        for tbl in ['LBF_AR_FM_1PUMP','LBF_AR_FM_2POWER','LBF_AR_FM_3SIZE','LBF_AR_FM_4BAR','LBF_AR_FM_5RLSZCL','LBF_AR_FM_6BARQTY','LBF_AR_FM_7SPECIAL1','LBF_AR_FM_8SENSOR','LBF_AR_FM_9SPL2']:
            subPartNumber = self.conTbl(tbl)
            Trace.Write(subPartNumber)
            if subPartNumber:
                if str(subPartNumber) != 'NONE':
                    cusPartNumber = cusPartNumber+str(subPartNumber)
            else:
                return 0
        # Trace.Write(self.count)
        # Trace.Write(cusPartNumber)
        if self.count == 9:
            self.createUpdatePartNumber(cusPartNumber)
        else:
            self.createUpdatePartNumber('')

object = Size().railSize()