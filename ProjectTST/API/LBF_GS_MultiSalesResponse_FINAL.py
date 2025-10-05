def update_MultiSalesQuote(data):
    res = []
    for obj in data:
        quoteNumber = obj["QuoteNumber"]
        status = obj["Status"]
        order_id = obj["Sales_Order_Id"]
        item_No = obj["Item_No"]
        S4SalesItmNo = obj["S4SalesOrderItemNumber"]
        partNumber = obj["PartNumber"]
        salesOrg = obj["SalesOrg"]
        quote = QuoteHelper.Get(str(quoteNumber))
        Log.Info(str(data))
        for item in quote.GetAllItems():
            if item.PartNumber == partNumber and item['LBF_QU_SalesOrg'] == salesOrg and str(item.RolledUpQuoteItem) == str(int(item_No // 10)):
                item['LBF_QU_SO_ORDERNO'] = order_id
                item['LBF_QU_SO_STATUS'] = "Order Created"
                item["LBF_QU_SO_ITEMNO"] = str(S4SalesItmNo)
        quote.Save()
        obj['CPQ_Status'] = "Order Created"
        res.append(obj)
    return res

if (Param is not None and Param.data is not None):
    data = JsonHelper.Serialize(Param.data)
    Log.Info("LBF_GS_MultiSalesResponse Param.data---->"+str(JsonHelper.Serialize(Param.data)))
    res = update_MultiSalesQuote(data)
    
    #url = RequestContext.Url
    #Log.Info(str(url))
    ApiResponse = ApiResponseFactory.JsonResponse(res)
else:
    Log.Info('Running')
    ApiResponse = ApiResponseFactory.JsonResponse("Failed")