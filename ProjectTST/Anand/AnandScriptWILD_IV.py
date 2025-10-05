Product.GetContainerByName('LBF_AR_WILDservC').Clear()
for conName in ['LBF_AR_WILDservC_LAB','LBF_AR_WILDservC_Truck','LBF_AR_WILDservC_PERD','LBF_AR_WILDservC_MISC']:
    Con1 = Product.GetContainerByName(conName)
    for data in Con1.Rows:
        if data.IsSelected == True:
            Con2 = Product.GetContainerByName('LBF_AR_WILDservC')
            newRow = Con2.AddNewRow(True)
            newRow['Costcat'] = str(data['Costcat'])
            newRow['Costtype'] = str(data['Costtype'])
            newRow['Subtype'] = str(data['Subtype'])
            newRow['Cost'] = str(data['Cost'])
            newRow['Unit'] = str(data['Unit'])
            newRow.Product.Attr('LBF_AR_WILDH3').AssignValue(str(data['TotalCost']))
            newRow['Margin'] = str(data['Margin'])
            newRow.Product.Attr('LBF_AR_WILDH2').AssignValue(str(data['Price']))
newRow.Calculate()






Product.GetContainerByName('LBF_AR_WILDservC').Clear()
Con1 = Product.GetContainerByName('LBF_AR_WILDservC_LAB')
for data in Con1.Rows:
    if data.IsSelected == True:
        Con2 = Product.GetContainerByName('LBF_AR_WILDservC')
        newRow = Con2.AddNewRow(True)
        newRow['Costcat'] = str(data['Costcat'])
        newRow['Costtype'] = str(data['Costtype'])
        newRow['Subtype'] = str(data['Subtype'])
        newRow['Cost'] = str(data['Cost'])
        newRow['Unit'] = str(data['Unit'])
        newRow.Product.Attr('LBF_AR_WILDH3').AssignValue(str(data['TotalCost']))
        newRow['Margin'] = str(data['Margin'])
        newRow.Product.Attr('LBF_AR_WILDH2').AssignValue(str(data['Price']))
newRow.Calculate()



Product.GetContainerByName('LBF_AR_WILDservC').Clear()
Con1 = Product.GetContainerByName('LBF_AR_WILDservC_MISC')
for data in Con1.Rows:
    if data.IsSelected == True:
        Con2 = Product.GetContainerByName('LBF_AR_WILDservC')
        newRow = Con2.AddNewRow(True)
        newRow['Costcat'] = str(data['Costcat'])
        newRow['Costtype'] = str(data['Costtype'])
        newRow['Subtype'] = str(data['Subtype'])
        newRow['Cost'] = str(data['Cost'])
        newRow['Unit'] = str(data['Unit'])
        newRow.Product.Attr('LBF_AR_WILDH3').AssignValue(str(data['TotalCost']))
        newRow['Margin'] = str(data['Margin'])
        newRow.Product.Attr('LBF_AR_WILDH2').AssignValue(str(data['Price']))
newRow.Calculate()


Product.GetContainerByName('LBF_AR_WILDservC').Clear()
Con1 = Product.GetContainerByName('LBF_AR_WILDservC_PERD')
for data in Con1.Rows:
    if data.IsSelected == True:
        Con2 = Product.GetContainerByName('LBF_AR_WILDservC')
        newRow = Con2.AddNewRow(True)
        newRow['Costcat'] = str(data['Costcat'])
        newRow['Costtype'] = str(data['Costtype'])
        newRow['Subtype'] = str(data['Subtype'])
        newRow['Cost'] = str(data['Cost'])
        newRow['Unit'] = str(data['Unit'])
        newRow.Product.Attr('LBF_AR_WILDH3').AssignValue(str(data['TotalCost']))
        newRow['Margin'] = str(data['Margin'])
        newRow.Product.Attr('LBF_AR_WILDH2').AssignValue(str(data['Price']))
newRow.Calculate()



Product.GetContainerByName('LBF_AR_WILDservC').Clear()
Con1 = Product.GetContainerByName('LBF_AR_WILDservC_Truck')
for data in Con1.Rows:
    if data.IsSelected == True:
        Con2 = Product.GetContainerByName('LBF_AR_WILDservC')
        newRow = Con2.AddNewRow(True)
        newRow['Costcat'] = str(data['Costcat'])
        newRow['Costtype'] = str(data['Costtype'])
        newRow['Subtype'] = str(data['Subtype'])
        newRow['Cost'] = str(data['Cost'])
        newRow['Unit'] = str(data['Unit'])
        newRow.Product.Attr('LBF_AR_WILDH3').AssignValue(str(data['TotalCost']))
        newRow['Margin'] = str(data['Margin'])
        newRow.Product.Attr('LBF_AR_WILDH2').AssignValue(str(data['Price']))
newRow.Calculate()