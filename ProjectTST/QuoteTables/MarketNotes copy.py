def sort_market_notes(qtTbl):
    data = []
    dup_data = {}
    for row in qtTbl.Rows:
        temp = {}
        Trace.Write(row['Note_Type'])
        temp[row['Note_Type']] = row['Notes']
        concat_notes = str(row['Note_Type'])+"|"+str(row['Notes'])
        if temp not in data:
            data.append(temp)
        elif concat_notes not in dup_data.keys():
            dup_data[concat_notes] = 2
        else:
            dup_data[concat_notes] = dup_data[concat_notes] + 1
        #Trace.Write(str(dup_data))
        
    sorted_data = sorted(data, key=lambda x: list(x.keys())[0])
    return sorted_data, dup_data

def quotetbl_update():
    quote = QuoteHelper.Get(str(context.Quote.QuoteNumber))
    qtTbl = quote.QuoteTables['Market_Notes']
    tot_sorted_data = sort_market_notes(qtTbl)
    sorted_data = tot_sorted_data[0]
    dup_data = tot_sorted_data[1]
    Trace.Write(str(dup_data))
    qtTbl.Rows.Clear()
    for row in sorted_data:
        for key, value in row.items():
            con_cat_notes = str(key)+"|"+str(value)
            if con_cat_notes not in dup_data:
                new_row = qtTbl.AddNewRow()
                new_row['Note_Type'] = key
                new_row['Notes'] = value
            else:
                for i in range(int(dup_data[con_cat_notes])):
                    new_row = qtTbl.AddNewRow()
                    new_row['Note_Type'] = key
                    new_row['Notes'] = value
    
quotetbl_update()
