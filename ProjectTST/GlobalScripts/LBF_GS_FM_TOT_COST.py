def fmUOMCost():
    for row in context.Quote.GetAllItems():
        Trace.Write(row.SelectedAttributes)
        for attr in row.SelectedAttributes:
            if attr.Name == "LBF_AT_FM_TOTALCOST":
                for val in attr.Values:
                    Trace.Write(val.Display)
                    row['LBF_QU_FM_COST'] = str(val.Display)

fmUOMCost()
