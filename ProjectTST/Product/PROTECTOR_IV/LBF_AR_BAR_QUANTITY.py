def barQty():
    pumpCon = Product.GetContainerByName('LBF_AR_FM_6BARQTY').Rows
    for row in pumpCon:
        row['Ext Cost'] = str(float(row['Cost']) * int(row['Qty']))

barQty()

