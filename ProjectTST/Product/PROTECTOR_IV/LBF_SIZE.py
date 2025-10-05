def size():
    pumpCon = Product.GetContainerByName('LBF_AR_FM_3SIZE').Rows
    for row in pumpCon:
        #Trace.Write(row['Code'])
        code = row['Code']
        sqlData = SqlHelper.GetFirst("select PARTNO,Code,Description from LBF_QU_FM_PROIV where PARTNO='{0}' and Code='{1}'".format('SIZE',code))
        #Trace.Write(row['Description'])
        row['Description'] = str(sqlData.Description)
        row['Ext Cost'] = str(float(row['Cost']) * int(row['Qty']))

size()