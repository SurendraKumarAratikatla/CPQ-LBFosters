for i in Product.Attributes:
    Trace.Write(i.SystemId)
    Trace.Write(i.DisplayType)
    Trace.Write(i.Access)
    count = 0
    for value in i.Values:
        if (value.IsSelected) == True:
            count += 1
            Trace.Write(value.IsSelected)
            Trace.Write(value.UserInput)
    if count == 0:
        Trace.Write("")


    Trace.Write("-------------------------------")
