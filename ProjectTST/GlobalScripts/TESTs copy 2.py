
def validation():
    try:
        if Product.Attr('PPK_AR_SHIPTO_ID').GetValue() == "New ShipTo":
            Product.Attr('PPK_AR_Destination').Access = AttributeAccess.Editable
        else:
            Product.Attr('PPK_AR_Destination').Access = AttributeAccess.ReadOnly
    except:
        pass

def attr_assign():
    validation()
    if Product.Attr('PPK_AR_Sales_Org').GetValue():
        Log.Info("In pass")
        return
    if context.Quote.SelectedMarket.Code == "1000":
        Product.Attr("PPK_AR_Sales_Org").SelectDisplayValue("1000 - North America")
        val = Product.Attr('PPK_AR_Sales_Org').GetValue()
        Query = SqlHelper.GetFirst("select Currency from PPK_SALES_ORG where Id_Name = '{0}'".format(str(val)))
        Product.Attr('PPK_AR_Currency').SelectDisplayValue(str(Query.Currency)) # PPK_AR_Volume_Escalation
        Product.Attr("PPK_AR_Sales_Org").Access = AttributeAccess.ReadOnly
        Product.Attr('PPK_AR_Currency').Access = AttributeAccess.ReadOnly

    else:
        Query = SqlHelper.GetFirst("select Id_Name from PPK_SALES_ORG where Id = '{}'".format(context.Quote.SelectedMarket.Code))
        Product.Attr("PPK_AR_Sales_Org").SelectDisplayValue(Query.Id_Name)
        val = Product.Attr('PPK_AR_Sales_Org').GetValue()
        Query = SqlHelper.GetFirst("select Currency from PPK_SALES_ORG where Id_Name = '{}'".format(val))
        Product.Attr('PPK_AR_Currency').SelectDisplayValue(Query.Currency)
        Product.Attr('PPK_AR_Currency').Access = AttributeAccess.ReadOnly

attr_assign()