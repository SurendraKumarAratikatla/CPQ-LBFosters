def segmentaions(val, components_con):
    # price = 0
    # cost = 0
    for row in components_con:
        #price = price + 0 if val == "0" else int(row[val])
        #cost = cost + 0 if row['cost'] == "0" else int(row['cost'])
        conComponent = row['Component']
        if conComponent == "Total":
            price = row[val]
            cost = row['cost']
            break
        #Trace.Write("----------------")
    Log.Info("price------->"+str(price))
    Log.Info("cost------->"+str(cost))
    Product.Attr('Temp_ListPrice').AssignValue(str(price))
    Product.Attr('Temp_Cost').AssignValue(str(cost))


def compComparision(custSegmentaion,components_con):
    if custSegmentaion == "High":
        segmentaions("High",components_con)
    elif custSegmentaion == "Medium":
        segmentaions("Medium",components_con)
    elif custSegmentaion == "Low":
        segmentaions("Low",components_con)
        #conComponent = row['Component']

custSegmentaion = Product.Attr('Customer Segmentation').SelectedValue
components_con = Product.GetContainerByName('Components').Rows
if custSegmentaion:
    compComparision(custSegmentaion.Display,components_con)