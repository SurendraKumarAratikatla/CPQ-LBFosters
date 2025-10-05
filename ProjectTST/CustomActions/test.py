def deleteQuoteMsgs():
    quoteInfo = QuoteHelper.Get(context.Quote.QuoteNumber)
    for msg in quoteInfo.Messages:
        if str(msg.Content) == "Items added successfully!" or str(msg.Content) == "Items not found for the provided reference quote number." or str(msg.Content) == "Invalid reference quote number, please check.":
            quoteInfo.DeleteMessage(msg.Id)
            # added comments

deleteQuoteMsgs()