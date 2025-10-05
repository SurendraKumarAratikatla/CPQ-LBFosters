# This script populates the Quote Table "Total_Summary" with Gross Profit values per Product Type.
# It maps values from item-level custom fields: LBF_QU_GP_PER and LBF_QU_GP_VAL
# to table-level columns: Gross_Profit_ (percent) and Gross_Profit_Margin_ (value)

def update_gp_table():
    quote_table = context.Quote.QuoteTables["Total_Summary"]
    quote_table.Rows.Clear()

    product_type_map = {}

    for item in context.Quote.GetAllItems():
        product_type = item.ProductTypeName

        gp_val = float(item["LBF_QU_GP_VAL"] or 0.0)
        gp_per = float(item["LBF_QU_GP_PER"] or 0.0)
        Tot_Cst = float(item["LBF_QU_TOTAL_COST"] or 0.0)
        Tot_Sp = float(item["LBF_QU_SELPRICE"] or 0.0)

        if product_type not in product_type_map:
            product_type_map[product_type] = {
                "Gross_Profit_Margin_": 0.0,
                "Gross_Profit_": 0.0,
                "Total_Cost":0.0,
                "Total_Price":0.0,
                "count": 0
            }

        product_type_map[product_type]["Gross_Profit_Margin_"] += gp_val
        product_type_map[product_type]["Gross_Profit_"] += gp_per
        product_type_map[product_type]["Total_Cost"] += Tot_Cst
        product_type_map[product_type]["Total_Price"] += Tot_Sp
        product_type_map[product_type]["count"] += 1

    for ptype, values in product_type_map.items():
        row = quote_table.AddNewRow()
        row["Product_Type"] = ptype
        row["Gross_Profit_Margin_"] = round(values["Gross_Profit_Margin_"], 2)
        row["Total_Cost"] = round(values["Total_Cost"], 2)
        row["Total_Price"] = round(values["Total_Price"], 2)
        if values["count"] > 0:
            row["Gross_Profit_"] = round(values["Gross_Profit_"] / values["count"], 2)
        else:
            row["Gross_Profit_"] = 0.0

update_gp_table()
