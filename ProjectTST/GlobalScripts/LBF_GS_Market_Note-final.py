notes_new_line = ["Prices quoted are subject to base price changes in metal/steel, and rubber, fuel, scrap, energy and other surcharges in effect at time of order placement and shipment.","CWR - Quoted from a Future Mill rolling. Subject to Mill acceptance, capacity and conditions at the time of order. Subject to Weld Plant conditions at the time of order."]
selected_market = context.Quote.SelectedMarket
selected_market_code = selected_market.Code

quoteNumber = context.Quote.QuoteNumber
quote = QuoteHelper.Get(str(quoteNumber))


def clear_table(table_name):
    table = quote.QuoteTables[table_name]
    table.Rows.Clear()
    quote.Save()


def sort_market_notes(qtTbl, data_list_obj):
    data_list = []
    for row in data_list_obj:
        temp_dict = {}
        temp_dict[row.Note_Type] = row.Note
        data_list.append(temp_dict)
    sorted_data_list = sorted(data_list, key=lambda x: list(x.keys())[0])
    return sorted_data_list


def populate_table(table_name):
    global notes_new_line
    table = quote.QuoteTables[table_name]
    query = "SELECT Note_Type, Note, Product FROM LBF_QU_NOTES WHERE Market_Code = '" + selected_market_code + "' and Product != 'CWR'"
    data_list_obj = SqlHelper.GetList(query)
    sorted_data_list = sort_market_notes(table, data_list_obj)
    Trace.Write(str(sorted_data_list))

    if sorted_data_list:
        for row in sorted_data_list:
            for key, value in row.items():
                new_row = table.AddNewRow()
                new_row['Note_Type'] = key
                new_row['Notes'] = str(value)+"\n" if value in notes_new_line else value
    else:
        Trace.Write("No matching entries found in LBF_QU_NOTES for the selected market code.")


#Clear both tables before adding data
clear_table('Market_Notes')
clear_table('Backend_Market_table')

# Populate both tables with same data
populate_table('Market_Notes')
populate_table('Backend_Market_table')



def populate_CWR_Notes(table_name):
    global notes_new_line
    table = context.Quote.QuoteTables[table_name]

    # BMQL/SQL needs quotes around literals in 2.7 (no params here)
    query = "SELECT Note, Note_Type FROM LBF_QU_NOTES WHERE Product = 'CWR'"
    result = SqlHelper.GetList(query)

    for data in result:
        # CPQ: create a new row, then set columns
        row = table.AddNewRow()  # or: table.Rows.AddNew() in some tenants

        row["Notes"] = str(data.Note)+"\n" if data.Note in notes_new_line else data.Note
        row["Note_Type"] = data.Note_Type
        if table_name == 'Backend_Market_table':
            row["Product"] = "CWR"
    return


# Run once if any CWR_QI item exists
has_cwr_qi = False
for it in context.Quote.GetAllItems():
    if it.ProductName == "CWR_QI":
        has_cwr_qi = True
        break
        
present_CWR = False

for i in context.Quote.QuoteTables['Backend_Market_table'].Rows:
    if i['Product'] == "CWR":
        present_CWR = True
        break

if has_cwr_qi and not present_CWR:
    # Will work for both tables as long as both define columns: Notes, Note_Type
    populate_CWR_Notes("Market_Notes")
    populate_CWR_Notes("Backend_Market_table")
