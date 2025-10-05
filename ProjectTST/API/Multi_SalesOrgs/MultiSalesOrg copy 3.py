import time
from LBF_GS_CREATEBEARERTOKEN import creating_bearer_token

class MultiSalesOrg():
    def __init__(self):
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

    def GetQuoteData(self):
        url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{}'.format(self.quoteInfo.Id)
        encodedKeys = "Bearer "+str(self.bearer_token)
        headers = {"Authorization":encodedKeys}
        quoteHeaderObj = RestClient.Get(url, headers)
        quoteHeaderStr = RestClient.SerializeToJson(quoteHeaderObj)
        quoteHeaderDataJson = RestClient.DeserializeJson(quoteHeaderStr)
        Trace.Write(quoteHeaderDataJson.QuoteId)
        Trace.Write(type(quoteHeaderDataJson))
        Trace.Write("quoteHeaderDataJson...............")
        Trace.Write(quoteHeaderDataJson)
        return quoteHeaderStr

    def GetCartItemData(self,itemId,itemConfig):
        url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{}/items/{}'.format(self.quoteInfo.Id,itemId)
        encodedKeys = "Bearer "+str(self.bearer_token)
        headers = {"Authorization":encodedKeys}
        itemDataObj = RestClient.Get(url, headers)
        itemDataStr = RestClient.SerializeToJson(itemDataObj)
        itemDataJson = RestClient.DeserializeJson(itemDataStr)
        Trace.Write(itemDataJson.ExternalConfigurationItemId)
        itemDataJson['ExternalConfiguration'] = itemConfig
        Trace.Write("GetCartItemData............")
        Trace.Write(itemDataJson)
        return itemDataStr

    def run(self):
        self.bearer_token = self.GetBearerToken()
        quoteData = self.GetQuoteData()
        self.Root['Quotes'] = quoteData
        cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/CPQInboundQuote_SalesOrder' # awaiting from CPI team
        for item in self.quoteInfo.GetAllItems():
            # get the individual data from quote header and one unique sales org item level data as per povided payload structure from CPI team
            itemId = item.Id
            itemConfig = RestClient.DeserializeJson(item.ExternalConfiguration)
            Trace.Write('itemConfig---->'+str(itemConfig))
            itemData = self.GetCartItemData(itemId,itemConfig)
            self.Root['QuoteItems'] = itemData
            Trace.Write(type(itemData))
            Trace.Write('itemData@@@@@@@@@@@@@'+str(itemData))
            requestData = {
                'Root':{
                    "Quotes":RestClient.DeserializeJson(quoteData),
                    "QuoteItems":RestClient.DeserializeJson(itemData)
                }
            }
            Log.Info('requestData---->'+str(requestData))
            #cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, requestData)
            #Trace.Write(str(cpiResponse))
            #cpiResponse = {'Sales Order ID':'64232325545','Quote#':'3434344','ItemNo':'1','ItemStatus':'Order Confirmed'}
            #time.sleep(1) # sleep 1 sec to send the payload as multiple times based on sales org type

object = MultiSalesOrg().run()