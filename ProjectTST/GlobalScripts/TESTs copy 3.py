Log.Info("Shipto running ")
Log.Info(Product.Attr('PPK_AR_Currency').GetValue())
Log.Info(Product.Attr("PPK_AR_Sales_Org").GetValue())
try:
    if Product.Attr('PPK_AR_SHIPTO_ID').GetValue() == "New ShipTo":
        Product.Attr('PPK_AR_Destination').Access = AttributeAccess.Editable
    else:
        Product.Attr('PPK_AR_Destination').Access = AttributeAccess.ReadOnly
except:
    pass
"""val = Product.Attr('PPK_AR_Sales_Org').GetValue()
if val is not None:
    pass
else:
if context.Quote.SelectedMarket.Code == "1000":
    Log.Info("in 1000")
    Product.Attr("PPK_AR_Sales_Org").SelectDisplayValue("1000 - North America")
    Product.Attr("PPK_AR_Sales_Org").Access = AttributeAccess.ReadOnly
    val = Product.Attr('PPK_AR_Sales_Org').GetValue()
    Query = SqlHelper.GetFirst("select Currency from PPK_SALES_ORG where Id_Name = '{}'".format(val))
    Product.Attr('PPK_AR_Currency').SelectDisplayValue(Query.Currency)
    #Log.Info(Product.Attr('PPK_AR_Curr').GetValue())
elif context.Quote.SelectedMarket.Code != "1000":
    if Product.Attr('PPK_AR_Sales_Org').GetValue():
        pass
    else:
        Log.Info("In else")
        Query = SqlHelper.GetFirst("select Id_Name from PPK_SALES_ORG where Id = '{}'".format(context.Quote.SelectedMarket.Code))
        Product.Attr("PPK_AR_Sales_Org").SelectDisplayValue(Query.Id_Name)
        val = Product.Attr('PPK_AR_Sales_Org').GetValue()
        Query = SqlHelper.GetFirst("select Currency from PPK_SALES_ORG where Id_Name = '{}'".format(val))
        Product.Attr('PPK_AR_Currency').SelectDisplayValue(Query.Currency)
        Product.Attr('PPK_AR_Currency').Access = AttributeAccess.ReadOnly"""