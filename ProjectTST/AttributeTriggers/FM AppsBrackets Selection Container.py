'''Product.GetContainerByName('FM AppsBrackets Selected lines Container').Clear()
for Con1 in ['FM AppsBrackets Selection Container']:
    conname = Product.GetContainerByName(Con1)
    for data in conname.Rows:
        if data.IsSelected == True:
            Con2 = Product.GetContainerByName('FM AppsBrackets Selected lines Container')
            newRow = Con2.AddNewRow(True)
#newRow = target.AddNewRow(True)

# Simulate a part number line item using custom fields (not real CPQ product)
newRow['PN'] = row['PN']
newRow['Description'] = row['Description']
newRow['Cost_of_20'] = row['Cost_of_20']
newRow['Qty'] = row['Qty']
newRow['Cost_CAD'] = row['Cost_CAD']
newRow['Site'] = row['Site']
newRow['IntercoMarkup'] = row['IntercoMarkup']
newRow['QuoteUnitCostCAD'] = row['QuoteUnitCostCAD']
newRow['ConverttoUSD'] = row['ConverttoUSD']
newRow['QuoteUnitCostUSD'] = row['QuoteUnitCostUSD']

# If going to the quote, assign this via QuoteItem-level fields:
# (Assumes 'PN' is used to set LBF_QU_PARTNUMBER or similar mapped field)

newRow.Product.Attr('LBF_AR_WILDH4').AssignValue(str(row['PN']))
newRow.Product.Attr('LBF_AR_WILDH1').AssignValue(str(row['Description']))
newRow.Product.Attr('LBF_AR_WILDH3').AssignValue(str(row['Cost_of_20']))
newRow.ApplyProductChanges()
newRow.Calculate()'''
Product.GetContainerByName('FM AppsBrackets Selected lines Container').Clear()
for Con1 in ['FM AppsBrackets Selection Container']:
    conname = Product.GetContainerByName(Con1)
    for data in conname.Rows:
        #Interco Markup % alone calculation
        intercoMarkup = 0
        if data['Site'] == 'VAN':
            intercoMarkup = (float(data['IntercoMarkup']) / 100) + 1
        
        #Qty alone calculation from PoweCurveCostRatio
        if data['Product_Type'] == 'Applicators':
            qtyData = SqlHelper.GetFirst("Select PoweCurveCostRatio, Qty from LBF_QU_FM_PCR_RA WHERE Qty ='{0}'".format(str(data['Qty'])))
        elif data['Product_Type'] == 'Brackets':
            qtyData = SqlHelper.GetFirst("Select PoweCurveCostRatio, Qty from LBF_QU_FM_PCR_RB WHERE Qty ='{0}'".format(str(data['Qty'])))
        
        # MAT COST
        #matCost = SqlHelper.GetFirst("Select PARTNUMBER, UNIT_COST_USD from LBF_QU_INFOR_MAT_COST WHERE PARTNUMBER ='{0}'".format(str(data['PN'])))

        if qtyData:
            pwrCostRatio = qtyData.PoweCurveCostRatio
            #COST Caculation based on QTY and Inter Markep % Cal
            if float(intercoMarkup) > 0:
                # data['Cost_CAD'] = str(float(matCost.UNIT_COST_USD) * float(intercoMarkup) * float(pwrCostRatio))
                data['Cost_CAD'] = str(float(data['Cost_of_20']) * float(intercoMarkup) * float(pwrCostRatio))
                Trace.Write("ifff")
                Trace.Write(intercoMarkup)
            else:
                # data['Cost_CAD'] = str(float(matCost.UNIT_COST_USD) * float(pwrCostRatio))
                data['Cost_CAD'] = str(float(data['Cost_of_20']) * float(pwrCostRatio))
                Trace.Write("elsee")


        if data.IsSelected == True:
            Con2 = Product.GetContainerByName('FM AppsBrackets Selected lines Container')
            newRow = Con2.AddNewRow(True)
            newRow['Qty'] = data['Qty']
            newRow['MatCost'] = data['Cost_CAD']
            #newRow['Site'] = data['Site']
            newRow['IntercoMarkup'] = data['IntercoMarkup']
            newRow['QuoteUnitCostCAD'] = data['QuoteUnitCostCAD']
            newRow['ConverttoUSD'] = data['ConverttoUSD']
            newRow['QuoteUnitCostUSD'] = data['QuoteUnitCostUSD']
            newRow['Currency'] = data['Currency']
            newRow.Product.Attr('LBF_AR_WILDH4').AssignValue(str(data['PN']))
            newRow.Product.Attr('ItemQuantity').AssignValue(str(data['Qty']))    		
            newRow.Product.Attr('LBF_AR_WILDH1').AssignValue(str(data['Description']))
            newRow.Product.Attr('LBF_AR_WILDH3').AssignValue(str(data['Cost_CAD']))
            newRow.Product.Attr('LBF_AR_WILDH5').AssignValue(str(data['Currency']))
            newRow.Product.Attr('LBF_AR_WILDH7').AssignValue(str(data['Site']))
            newRow.ApplyProductChanges()
            newRow.Calculate()