Log.Info("Shipto running ")
try:
    if Product.Attr('PPK_AR_SHIPTO_ID').GetValue() == "New ShipTo":
        Product.Attr('PPK_AR_Destination').Access = AttributeAccess.Editable
    else:
        Product.Attr('PPK_AR_Destination').Access = AttributeAccess.ReadOnly
except:
    pass
# if Product.Attr('PPK_AR_Sales_Org').GetValue():
#     Log.Info("In pass")
#     pass
# else:

ar_sales_org = Product.Attr('PPK_AR_Sales_Org').GetValue()

if ar_sales_org is None and context.Quote.SelectedMarket.Code == "1000":
    Log.Info("in 1000")
    Product.Attr("PPK_AR_Sales_Org").SelectDisplayValue("1000 - North America")
    Product.Attr("PPK_AR_Sales_Org").Access = AttributeAccess.ReadOnly
    val = Product.Attr('PPK_AR_Sales_Org').GetValue()
    Query = SqlHelper.GetFirst("select Currency from PPK_SALES_ORG where Id_Name = '{}'".format(val))
    Log.Info(Query.Currency)
    Product.Attr('PPK_AR_Currency').SelectDisplayValue(Str(Query.Currency)) # PPK_AR_Volume_Escalation
    #Product.Attr('PPK_AR_Volume_Escalation').SelectDisplayValue("USD")
    Log.Info(Product.Attr('PPK_AR_Currency').GetValue())
    Product.Attr('PPK_AR_Currency').Access = AttributeAccess.ReadOnly

elif ar_sales_org is None and context.Quote.SelectedMarket.Code != "1000":
    Query = SqlHelper.GetFirst("select Id_Name from PPK_SALES_ORG where Id = '{}'".format(context.Quote.SelectedMarket.Code))
    Product.Attr("PPK_AR_Sales_Org").SelectDisplayValue(Query.Id_Name)
    val = Product.Attr('PPK_AR_Sales_Org').GetValue()
    Query = SqlHelper.GetFirst("select Currency from PPK_SALES_ORG where Id_Name = '{}'".format(val))
    Product.Attr('PPK_AR_Currency').SelectDisplayValue(Query.Currency)
    Product.Attr('PPK_AR_Currency').Access = AttributeAccess.ReadOnly