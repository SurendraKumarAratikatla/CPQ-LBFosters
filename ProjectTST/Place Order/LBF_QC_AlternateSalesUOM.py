from Scripting.Quote import MessageLevel

items = context.AffectedItems

for item in items:
    partNumber = item.PartNumber
    Log.Info('partNumber->' + partNumber)
    if item.ProductName != 'CWR' and item.ProductName != 'CWR_QI':
        query1 = "select gross_weight, sap_cost, WEIGHT_UNIT from LBF_QU_MAT_COST where MATERIAL = '{0}'".format(partNumber)

        data1 = SqlHelper.GetFirst(query1)
        
        Log.Info(str(data1))

        if data1:
            gross_weight = data1.gross_weight
            cost = data1.sap_cost
            unit1 = data1.WEIGHT_UNIT
            unit2 = item['LBF_QU_TARUOM']
            
            
                
            Log.Info('Default- ' + unit1)
            Log.Info('Curr- ' + unit2)

            if unit1 != unit2:

                query2 = "select unit1, unit2, target, input from LBF_QU_WT_CAL where unit1 = '{0}' and unit2 = '{1}'".format(unit1, unit2)

                data2 = SqlHelper.GetFirst(query2)
                
                
                
                if data2:
                    
                    conversion = float(data2.input) / float(data2.target)

                    mat_val = ((float(conversion * item.Quantity))/ float(gross_weight))* float(cost)
                    
                    Log.Info('Mat Info' + str(mat_val))

                    item['LBF_QU_MAT_CST'] = mat_val / item.Quantity
                    
                    Log.Info(str(item['LBF_QU_MAT_CST']))
                    
                    item['LBF_QU_ExtCost'] = mat_val