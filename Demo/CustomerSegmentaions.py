def segmentaions(val, components_con):
    price = 0
    cost = 0
    for row in components_con:
        #price = price + 0 if val == "0" else int(row[val])
        #cost = cost + 0 if row['cost'] == "0" else int(row['cost'])
        if row[val]:
            price = price + int(row[val])
        if row['cost']:
            cost = cost + int(row['cost'])
        #Trace.Write("----------------")
    #Trace.Write("price------->"+str(price))
    #Trace.Write("cost------->"+str(cost))
    currentItem = Product.ParseString('<*CTX( Quote.CurrentItem.RolledUpItemNumber )*>')

    for item in context.Quote.GetAllItems():
        Trace.Write("############################")
        if str(item.RolledUpQuoteItem) == str(currentItem):
            item["LBF_Price"] = str(price)
            item["LBF_Cost"] = str(cost)
            Trace.Write("@@@@@@@@@@@@@@@@@@@@@------->")

        break
    # price, cost
    pass
def compComparision(custSegmentaion,components_con):
    if custSegmentaion == "High":
        segmentaions("High",components_con)
    elif custSegmentaion == "Medium":
        segmentaions("Medium",components_con)
    elif custSegmentaion == "Low":
        segmentaions("Low",components_con)
        #conComponent = row['Component']

custSegmentaion = Product.Attr('Customer Segmentation').SelectedValue.Display
components_con = Product.GetContainerByName('Components').Rows
if custSegmentaion:
    compComparision(custSegmentaion,components_con)