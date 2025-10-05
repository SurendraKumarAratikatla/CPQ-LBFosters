# Create/ update into the profit center summary quote table
def update_profcenter_table():
    quote_table = context.Quote.QuoteTables["ProfitCenter_Summary"]
    quote_table.Rows.Clear()
    profit_center_map = {}
    cf_quoteTot_voilated = context.Quote.GetCustomField('LBF_CF_QuoteTotal_Voilated').Value
    cf_margin_voilated = context.Quote.GetCustomField('LBF_CF_QuoteMargin_Voilated').Value

    for item in context.Quote.GetAllItems():
        profit_center = item["LBF_QU_ProfitCenter"]
        sel_price = float(item["LBF_QU_SELPRICE"] or 0.0)
        gp_val = float(item["LBF_QU_GP_VAL"] or 0.0)

        if profit_center not in profit_center_map:
            profit_center_map[profit_center] = {
                "Profit_Center": "",
                "Total_Cell_Price": 0.0,
                "Margin_Value":0.0,
            }

        profit_center_map[profit_center]["Total_Cell_Price"] += sel_price
        profit_center_map[profit_center]["Margin_Value"] += gp_val

    for pcenter, values in profit_center_map.items():
        row = quote_table.AddNewRow()
        row["profit_center"] = pcenter
        row["Total_Cell_Price"] = round(values["Total_Cell_Price"], 2)
        row["Margin_Value"] = round(values["Margin_Value"], 2)
        if not cf_quoteTot_voilated and not cf_margin_voilated:
            set_flag_for_approvals(pcenter, row["Total_Cell_Price"], row["Margin_Value"])

# Wrokflows & Approval setting flag for profitcenters and margin value
def set_flag_for_approvals(pcenter, sellprice, marginval):
    data = SqlHelper.GetFirst("Select ProfitCenter,QuoteTotal,QuoteMargin from LBF_QU_APPROVALMATRIX where ProfitCenter ='{0}'".format(pcenter)) 
    if data:
        if float(data.QuoteTotal) < float(sellprice):
            context.Quote.GetCustomField('LBF_CF_QuoteTotal_Voilated').Value = "True"
             
        elif float(data.QuoteMargin) < float(marginval):
            context.Quote.GetCustomField('LBF_CF_QuoteMargin_Voilated').Value = "True"
    

update_profcenter_table()
