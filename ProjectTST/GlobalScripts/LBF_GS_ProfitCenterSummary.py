def update_profcenter_table():
    quote_table = context.Quote.QuoteTables["ProfitCenter_Summary"]
    quote_table.Rows.Clear()

    profit_center_map = {}

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


update_profcenter_table()
