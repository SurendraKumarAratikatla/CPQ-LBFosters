def calculate_gross_profit_percent(selling_price, total_cost): 
    if selling_price == 0:
        return 0.0
    gross_profit_percent = ((selling_price - total_cost) / selling_price) * 100
    return gross_profit_percent

#items = context.Quote.GetAllItems()  # Use this for Workbench execution
items = context.AffectedItems

for item in items:
    #try:
    selling_price = float(item['LBF_QU_SELPRICE_UN'])
    quantity = float(item.Quantity)
    total_cost = float(item['LBF_QU_TOTAL_COST']) / quantity if quantity != 0 else 0.0
    item['LBF_QU_GP_PER'] = float(calculate_gross_profit_percent(selling_price, total_cost))

    item['LBF_QU_SELPRICE'] = str(round(selling_price * quantity, 2))
    gross_profit_value = (selling_price - total_cost) * quantity
    item['LBF_QU_GP_VAL'] = str(round(gross_profit_value, 2))
    #Log.Write(f"Item {item.ProductId}: GP% = {profit}, Total Sell Price = {item['LBF_QU_SELPRICE']}")
    Log.Info('LBF_QC_GrossProfitCalculation In Try')

    '''except Exception as e:
        Log.Info('LBF_QC_GrossProfitCalculation In except')
        #Log.Write(f"Error on item {item.ProductId}: {str(e)}")
        item['LBF_QU_GP_PER'] = 0.0
        item['LBF_QU_SELPRICE'] = "0.00"
        Log.Info('LBF_QC_GrossProfitCalculation Error....in '+str(e))'''