selected_market = context.Quote.SelectedMarket
selected_market_code = selected_market.Code

quoteNumber = context.Quote.QuoteNumber
quote = QuoteHelper.Get(str(quoteNumber))

def clear_market_update_table():
    market_update_table = quote.QuoteTables['Market_Notes']
    market_update_table.Rows.Clear()
    quote.Save()

def sort_market_notes(qtTbl,data_list_obj):
    data_list = []
    for row in data_list_obj:
        temp_dict = {}
        temp_dict[row.Note_Type] = row.Note
        data_list.append(temp_dict)
    sorted_data_list = sorted(data_list, key=lambda x: list(x.keys())[0])
    return sorted_data_list

def populate_market_update_table():
    market_update_table = quote.QuoteTables['Market_Notes']
    query = "SELECT Note_Type, Note FROM LBF_QU_NOTES WHERE Market_Code = '" + selected_market_code + "'"
    data_list_obj = SqlHelper.GetList(query)
    sorted_data_list = sort_market_notes(market_update_table,data_list_obj)
    Trace.Write(str(sorted_data_list))
    if sorted_data_list:
        for row in sorted_data_list:
            for key, value in row.items():
                new_row = market_update_table.AddNewRow()
                new_row['Note_Type'] = key
                new_row['Notes'] = value
    else:
        Trace.Write("No matching entries found in LBF_QU_NOTES for the selected market code.")

clear_market_update_table()
populate_market_update_table()