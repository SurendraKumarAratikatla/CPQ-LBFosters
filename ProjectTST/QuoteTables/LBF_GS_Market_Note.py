selected_market = context.Quote.SelectedMarket
selected_market_code = selected_market.Code

quoteNumber = context.Quote.QuoteNumber
quote = QuoteHelper.Get(str(quoteNumber))

def clear_market_update_table():
    market_update_table = quote.QuoteTables['Market_Notes']
    market_update_table.Rows.Clear()
    quote.Save()

def populate_market_update_table():
    market_update_table = quote.QuoteTables['Market_Notes']
    
    query = "SELECT Note_Type, Note FROM LBF_QU_NOTES WHERE Market_Code = '" + selected_market_code + "'"
    data_list = SqlHelper.GetList(query)
    Trace.Write("Data List: " + str(data_list))
    
    if data_list:
        for row in data_list:
            Trace.Write("Row: " + str(row))
            new_row = market_update_table.AddNewRow()
            new_row['Note_Type'] = getattr(row, 'Note_Type', None)
            new_row['Notes'] = getattr(row, 'Note', None)
            #Trace.Write("New Row: Note Type - " + str(new_row['Note_Type']) + ", Note - " + str(new_row['Note']))
        quote.Save()
    else:
        Trace.Write("No matching entries found in LBF_QU_NOTES for the selected market code.")

clear_market_update_table()
populate_market_update_table()