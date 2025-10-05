def update_MultiSalesQuote(data):
    res = []
    Log.Info("innnn00000000")
    for obj in data:
        Log.Info(str(obj))
        Log.Info("innnn1111111")
        quoteNumber = obj["QuoteNumber"]
        status = obj["Status"]
        order_id = obj["Sales_Order_Id"]
        #item_No = obj["Item_No"]
        S4SalesItmNo = obj["S4SalesOrderItemNumber"]
        partNumber = obj["PartNumber"]
        salesOrg = obj["SalesOrg"]
        quote = QuoteHelper.Get(str(quoteNumber))
        Log.Info(str(data))
        count = 0
        for item in quote.GetAllItems():
            Log.Info("item.RolledUpQuoteItem-->"+str(item.RolledUpQuoteItem))
            Log.Info("str(int(item_No // 10))-->"+str(int(S4SalesItmNo) // 10))
            if str(item.RolledUpQuoteItem) == str(int(S4SalesItmNo) // 10):
                Log.Info("innnn22222222")
                item['LBF_QU_SO_ORDERNO'] = order_id
                item['LBF_QU_SO_STATUS'] = "Order Created"
                item["LBF_QU_SO_ITEMNO"] = str(S4SalesItmNo)
            
            if str(item['LBF_QU_SO_STATUS']) != "Order Created" and str(item['LBF_QU_SO_STATUS']) != "Invalid S/4 Material":
                count += 1
        quote.Save()
        obj['CPQ_Status'] = "Order Created"
        res.append(obj)
        Log.Info("count--->"+str(count))
        if count == 0:
            Log.Info("count in if--->"+str(count))
            quote.ChangeStatus('Order Placed')
    return res

if (Param is not None and Param.data is not None):
    data = JsonHelper.Serialize(Param.data)
    Log.Info("LBF_GS_MultiSalesResponse Param.data---->"+str(JsonHelper.Serialize(Param.data)))
    res = update_MultiSalesQuote(Param.data)
    
    #url = RequestContext.Url
    #Log.Info(str(url))
    ApiResponse = ApiResponseFactory.JsonResponse(res)
else:
    Log.Info('Running')
    ApiResponse = ApiResponseFactory.JsonResponse("Failed")