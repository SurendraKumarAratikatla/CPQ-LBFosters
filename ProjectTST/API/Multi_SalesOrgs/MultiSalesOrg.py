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
        serializedQuote_data = JsonHelper.Serialize(quoteHeaderObj)
        quoteHeaderJSON = JsonHelper.Deserialize(serializedQuote_data)
        return quoteHeaderJSON

    def GetCartItemData(self,itemId,itemConfig):
        url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{}/items/{}'.format(self.quoteInfo.Id,itemId)
        encodedKeys = "Bearer "+str(self.bearer_token)
        headers = {"Authorization":encodedKeys}
        itemDataObj = RestClient.Get(url, headers)
        serializedItem_data = JsonHelper.Serialize(itemDataObj)
        quoteHeaderJSON = JsonHelper.Deserialize(serializedItem_data)
        quoteHeaderJSON['ExternalConfiguration'] = itemConfig
        return quoteHeaderJSON

    def run(self):
        self.bearer_token = self.GetBearerToken()
        quoteData = self.GetQuoteData()
        self.Root['Quotes'] = quoteData
        cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/CPQInboundQuote_SalesOrder' # awaiting from CPI team
        for item in self.quoteInfo.GetAllItems():
            # get the individual data from quote header and one unique sales org item level data as per povided payload structure from CPI team
            itemId = item.Id
            # Trace.Write('itemConfig---->'+str(itemConfig))
            itemConfig = JsonHelper.Deserialize(item.ExternalConfiguration)
            quoteitemData = self.GetCartItemData(itemId,itemConfig)

            requestData = {
                'Root':{
                    "QuoteHeader":quoteData,
                    "QuoteItems":quoteitemData
                }
            }
            Log.Info('MultiSales org requestData from CPQ to cpi---->'+str(requestData))
            try:
                cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, requestData)
            except Exception as e:
                Log.Info('Error: Multi sales org as...: '+str(e))
            #Trace.Write(str(cpiResponse))
            # cpiResponse = {'Sales Order ID':'64232325545','Quote#':'3434344','ItemNo':'1','ItemStatus':'Order Confirmed'}
            time.sleep(1) # sleep 1 sec to send the payload as multiple times based on sales org type

object = MultiSalesOrg().run()