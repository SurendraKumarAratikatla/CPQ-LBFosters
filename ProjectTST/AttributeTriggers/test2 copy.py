from LBF_GS_CREATEBEARERTOKEN import creating_bearer_token

class MultiSalesOrg:
    def __init__(self):
        # self.params = params
        self.quoteInfo = QuoteHelper.Get(context.Quote.QuoteNumber)
        self.bearer_token = ''
        self.headerStack = {}
        self.ItemStack = {}
        self.Root = {}

    def GetBearerToken(self):
        response = creating_bearer_token()
        if response[1] == 'success':
            stream = RestClient.DeserializeJson(StreamReader(response[0].GetResponseStream()).ReadToEnd())
            return stream.access_token
        else:
            return 'error'
            
    def GetCartItemData(self):
        quoteInfo = QuoteHelper.Get(context.Quote.QuoteNumber)
        self.bearer_token = self.GetBearerToken()
        url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{}/items'.format(quoteInfo.Id)
        encodedKeys = "Bearer " + str(self.bearer_token)
        headers = {"Authorization": encodedKeys}
        itemDataObj = RestClient.Get(url, headers)
        ser_data = JsonHelper.Serialize(itemDataObj)
        deser_data = JsonHelper.Deserialize(ser_data)
        Trace.Write(deser_data[0]['CustomFields'])
        for row in deser_data[0]['CustomFields']:
            if row['Name'] == "LBF_QU_Notes":
                row['Content'] = row['Content'].replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace("–","–").replace("—","—")
                Trace.Write(row['Content'])
        Trace.Write(str(type(itemDataObj)))
        Trace.Write(str(type(ser_data)))
        Trace.Write(str(type(deser_data)))

        return itemDataObj
    
object = MultiSalesOrg().GetCartItemData()