def sort_market_notes(qtTbl):
    data = []
    for row in qtTbl.Rows:
        temp = {}
        Trace.Write(row['Note_Type'])
        temp[row['Note_Type']] = row['Notes']
        data.append(temp)

    key_order = []
    for item in data:
        key = list(item.keys())[0]
        if key not in key_order:
            key_order.append(key)
    
    order_map = {key: i for i, key in enumerate(key_order)}
    sorted_data = sorted(data,key=lambda d: (order_map[list(d.keys())[0]], list(d.values())[0].lower()))
    return sorted_data

    # Trace.Write(str(data))
    # sorted_data = sorted(data, key=lambda d: list(d.keys())[0])
    # #sorted_data = sorted(data, key=lambda d: (list(d.keys())[0], list(d.values())[0]))
    # return sorted_data


def quotetbl_update():
    quote = QuoteHelper.Get(str(context.Quote.QuoteNumber))   
    qtTbl = quote.QuoteTables['Market_Notes']
    sorted_data = sort_market_notes(qtTbl)
    qtTbl.Rows.Clear()
    for row in sorted_data:
        for key, value in row.items():
            new_row = qtTbl.AddNewRow()
            new_row['Note_Type'] = key
            new_row['Notes'] = value
    
quotetbl_update()
