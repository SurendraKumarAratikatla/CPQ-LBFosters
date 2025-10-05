customFields = ""
poDate = context.Quote.GetCustomField("LBF_CF_PODATE").Value # LBF_CF_PODATE
inco1 = context.Quote.GetCustomField("LBF_CF_INCOTERMS").Value
inco2 = context.Quote.GetCustomField("LBF_CF_INCOTERMS2").Value
payTerms = context.Quote.GetCustomField("LBF_CF_PAYTERMS").Value
poNumber = context.Quote.GetCustomField("LBF_CF_PONUMBER").Value

if poDate == '' or poDate == '0':
    customFields += "PO Date, "
if inco1 == '0' or inco1 == '':
    customFields += "incoterms, "
if inco2 == '' or inco2 == '0':
    customFields += "incoterms1, "
if payTerms == '0' or payTerms == '':
    customFields += "Payment Terms, "
if poNumber == '' or poNumber == '0':
    customFields += "PO Number, "




'''LBF_CF_INCOTERMS
LBF_CF_INCOTERMS2
LBF_CF_PAYTERMS
LBF_CF_PONUMBER'''


tot_attr = Product.Attributes
for item in tot_attr:
    values = item.Values
    for value in values:
        if value.IsSelected == True:
            valueCode = str(value.ValueCode)
            value = str(value.UserInput) if valueCode == "DefaultValue" else valueCode
            Trace.Write(value)




tot_attr = Product.Attributes
dictStack = {}
for item in tot_attr:
    values = item.Values
    attrName = item.Name
    for value in values:
        if value.IsSelected == True:
            dictStack[attrName] = value.UserInput

Trace.Write(str(dictStack))


tot_attr = Product.Attributes
dictStack = []
for item in tot_attr:
    values = item.Values
    attrName = item.Name
    for value in values:
        if value.IsSelected == True:
            dictStack.append((attrName,value.UserInput))

Trace.Write(str(dictStack))



tot_attr = Product.Attributes
tupleStack = []
for item in tot_attr:
    values = item.Values
    attrName = item.Name
    for value in values:
        if value.IsSelected == True:
            tupleStack.append((attrName,value.UserInput))

Trace.Write(str(tupleStack))

for i,j in tupleStack:
    Trace.Write(i)