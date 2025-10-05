components_con = Product.GetContainerByName('Components').Rows
qtyList = {}
for row in components_con:
    if row['Component'] == "Lidar" or row['Component'] == "Control panel" or row['Component'] == "Men" or row['Component'] == "CCTV":
    	qtyList[str(row['Component'])] = int(row['Qty'])
Trace.Write(str(qtyList))