from Scripting.Quote import MessageLevel

def VCPReqFieldsChangeMsg():
    count = 0
    qtMsg = "Plant, Quantity, or UOM has changed. Please update the configuration for the highlighted row."
    cu_quote = QuoteHelper.Get(context.Quote.QuoteNumber)
    for msg in cu_quote.Messages:
        count += 1
        if str(msg.Content) != str(qtMsg):
            Trace.Write(msg.Content)
            cu_quote.AddMessage(str(qtMsg), MessageLevel.Error, False)
            break

    for item in context.AffectedItems:
        partNumber = item.PartNumber
        vcpPro = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(partNumber,'True','False'))
        if vcpPro and count == 0:
            cu_quote.AddMessage(str(qtMsg), MessageLevel.Error, False)
            item['LBF_QU_IsVCPFieldsChanged'] = 'Yes'
            
VCPReqFieldsChangeMsg()