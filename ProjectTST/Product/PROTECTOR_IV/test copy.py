def specials2():
    pumpCon = Product.GetContainerByName('LBF_AR_FM_9SPL2').Rows
    for row in pumpCon:
        #Trace.Write(row['Code'])
        code = row['Code']
        sqlData = SqlHelper.GetFirst("select PARTNO,Code,Description from LBF_QU_FM_PROIV where PARTNO='{0}' and Code='{1}'".format('SPECIAL-II',code))
        #Trace.Write(row['Description'])
        if sqlData:
            row['Description'] = str(sqlData.Description)
            row['Ext Cost'] = str(float(row['Cost']) * int(row['Qty']))
            currTotal = float(Product.Attr('LBF_AT_FM_TOTALCOST').GetValue()) + float(row['Ext Cost'])
            Product.Attr('LBF_AT_FM_TOTALCOST').AssignValue(str(currTotal))

specials2()