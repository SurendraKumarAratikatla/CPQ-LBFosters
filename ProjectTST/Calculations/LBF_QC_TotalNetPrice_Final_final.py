items = context.Quote.GetAllItems()

quote = QuoteHelper.Get(context.Quote.Id)

selling_price = 0.0

for item in items:
    item_ = quote.GetItemByItemId(item.Id)
    itemTypeOpt = item.AsMainItem.IsOptional
    itemTypeAlt = item.AsMainItem.IsAlternative
    itemTypeVar = item.AsMainItem.IsVariant
    if itemTypeOpt == False and itemTypeAlt == False and itemTypeVar == False:
        #Trace.Write('item type is Base')
        if item_['LBF_QU_SELPRICE']:
            selling_price = selling_price + item_['LBF_QU_SELPRICE']
    
if int(selling_price):
    context.Quote.Totals.Amount = selling_price