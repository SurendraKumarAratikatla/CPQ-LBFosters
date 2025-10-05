def fmUOMCost():
    updated = False
    for item in context.AffectedItems:
        if item.ProductName == "PROTECTOR IV" and updated == False:
            Trace.Write(item.SelectedAttributes)
            for attr in item.SelectedAttributes:
                if attr.Name == "LBF_AT_FM_TOTALCOST":
                    for val in attr.Values:
                        if val:
                            Trace.Write(val.Display)
                            item['LBF_QU_FM_COST'] = str(val.Display)
                            updated = True
        else:
            break

fmUOMCost()