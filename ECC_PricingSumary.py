def pricingsumary():
    quotetable = context.Quote.QuoteTables["PricingConditions"]
    quotetable.Rows.Clear()
    lineitemlist = []
    itemNums = context.Quote.GetCustomField('CFH_ItemNumbers').Value
    itemNumList = [itemNum for itemNum in itemNums]
    for mainItem in context.Quote.GetAllItems():
        rolledUpItemNum = mainItem.RolledUpQuoteItem
        if (rolledUpItemNum[0] in itemNumList):
            lineitemlist.append(mainItem.RolledUpQuoteItem)
        # Log.Info(len(mainItem.RolledUpQuoteItem))
        Log.Info("1111111111111111")
    for mainItem in context.Quote.GetAllItems():
        rolledUpItemNum = mainItem.RolledUpQuoteItem
        Log.Info("rolledUpItemNum--->"+str(rolledUpItemNum))
        Log.Info("itemNumList--->"+str(itemNumList))
        if (rolledUpItemNum[0] in itemNumList):
            # Trace.Write(rolledUpItemNum)
            #if mainItem.ParentItemId == 0:
            #Trace.Write(mainItem.RolledUpQuoteItem)
            pricingcount = 0
            flag = 'false'
            Log.Info(pricingcount)
            discountcount = 0
            if len(mainItem.RolledUpQuoteItem) == 1:
                total = float(mainItem.VCPricingPayload.NetValue) + float(mainItem.VCPricingPayload.TaxValue)
            #try:
            for i in mainItem.VCItemPricingPayload.Conditions:
                #Trace.Write(str(i.ConditionTypeDescription))
                Log.Info("{0} ".format(i.ConditionValue))
                #Trace.Write("{0} ".format(i.CalculationType))
                if i.ConditionType == "PR00" or i.ConditionType == "VA00" or i.ConditionTypeDescription == 'Gross Value':
                    #Trace.Write("{0} ".format(i.ConditionUnitValue))
                    if pricingcount == 0 and i.ConditionType != '' and i.ConditionTypeDescription != '':
                        pricingcount += 1
                        row = quotetable.AddNewRow()
                        row['Item'] = str(mainItem.RolledUpQuoteItem)
                        row['Material_Description'] = str(mainItem.Description)
                        row['Condition_Type'] = str(i.ConditionTypeDescription)
                        row['Amount'] = str(i.ConditionRate)
                        row['Currency'] = str(i.ConditionCurrency)
                        row['Per'] = str(i.ConditionUnitValue)
                        row['UOM'] = str(i.ConditionUnit)
                        row['Condition_Value'] = str(i.ConditionValue)
                    else:
                        if i.ConditionType:
                            row = quotetable.AddNewRow()
                            #row['Item'] = str(mainItem.RolledUpQuoteItem)
                            #row['Material_Description'] = str(mainItem.Description)
                            row['Condition_Type'] = str(i.ConditionTypeDescription)
                            row['Amount'] = str(i.ConditionRate)
                            row['Currency'] = str(i.ConditionCurrency)
                            row['Per'] = str(i.ConditionUnitValue)
                            row['UOM'] = str(i.ConditionUnit)
                            row['Condition_Value'] = str(i.ConditionValue)
                        if i.ConditionTypeDescription == 'Gross Value':
                            row = quotetable.AddNewRow()
                            #row['Item'] = str(mainItem.RolledUpQuoteItem)
                            #row['Material_Description'] = str(mainItem.Description)
                            row['Condition_Type'] = str(i.ConditionTypeDescription)
                            row['Amount'] = str(i.ConditionRate)
                            row['Currency'] = str(i.ConditionCurrency)
                            row['Per'] = str(i.ConditionUnitValue)
                            row['UOM'] = str(i.ConditionUnit)
                            row['Condition_Value'] = str(i.ConditionValue)
                if i.CalculationType == 'A' or i.ConditionTypeDescription == "Discount Amount":
                    #Trace.Write("{0} ".format(i.ConditionTypeDescription))
                    if discountcount == 0:
                        #Trace.Write('check')
                        Log.Info(mainItem.RolledUpQuoteItem)
                        discountcount += 1
                        row = quotetable.AddNewRow()
                        row['Material_Description'] = 'Discounts'
                        if i.ConditionType:
                            row = quotetable.AddNewRow()
                            row['Condition_Type'] = str(i.ConditionTypeDescription+i.ConditionRate+'%')
                            row['Currency'] = str(i.ConditionCurrency)
                            row['Condition_Value'] = str(i.ConditionValue)
                        if i.ConditionTypeDescription == "Discount Amount":
                            row = quotetable.AddNewRow()
                            row['Material_Description'] = 'Discount Amount'
                            row['Condition_Value'] = str(i.ConditionValue)
                    else:
                        #Trace.Write("{0} ".format(i.ConditionCurrency))
                        if i.ConditionType:
                            row = quotetable.AddNewRow()
                            #row['Item'] = str(mainItem.RolledUpQuoteItem)
                            #row['Material_Description'] = str(mainItem.Description)
                            row['Condition_Type'] = str(i.ConditionTypeDescription)
                            row['Currency'] = str(i.ConditionCurrency)
                            row['Condition_Value'] = str(i.ConditionValue)
                        if i.ConditionTypeDescription == 'Discount Amount':
                            #Trace.Write("cc==" +str(i.ConditionTypeDescription))
                            #Trace.Write(i.ConditionValue)
                            row = quotetable.AddNewRow()
                            row['Material_Description'] = str(i.ConditionTypeDescription)
                            row['Condition_Value'] = str(i.ConditionValue)
                if i.ConditionTypeDescription == 'Net Value for Item':
                    row = quotetable.AddNewRow()
                    row['Material_Description'] = 'Net Value'
                    row['Condition_Value'] = str(i.ConditionValue)
            #except Exception as ex:
            #    Trace.Write(ex)
            '''if len(mainItem.RolledUpQuoteItem) == 3:
                line = float(mainItem.RolledUpQuoteItem)+0.1
                if str(line) not in lineitemlist:
                    row = quotetable.AddNewRow()
                    row['Material_Description'] = 'Total'
                    row['Condition_Value'] = str(total)'''
            line = float(mainItem.RolledUpQuoteItem)+0.1
            if len(mainItem.RolledUpQuoteItem) == 3:
                line = float(mainItem.RolledUpQuoteItem)+0.1
                if str(line) not in lineitemlist:
                    row = quotetable.AddNewRow()
                    row['Material_Description'] = 'Total'
                    row['Condition_Value'] = str(total)
            elif str(line) not in lineitemlist:
                row = quotetable.AddNewRow()
                row['Material_Description'] = 'Total'
                row['Condition_Value'] = str(total)
usertype = User.UserType.Name
company = User.Company.Id
if (usertype == 'Sales' or usertype == 'Sales Management') and company == 17:
    pricingsumary()