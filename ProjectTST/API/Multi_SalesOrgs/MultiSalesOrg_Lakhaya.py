import time
from LBF_GS_CREATEBEARERTOKEN import creating_bearer_token
from Scripting.Quote import MessageLevel

class MultiSalesOrg:
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
        encodedKeys = "Bearer " + str(self.bearer_token)
        headers = {"Authorization": encodedKeys}
        quoteHeaderObj = RestClient.Get(url, headers)
        serializedQuote_data = JsonHelper.Serialize(quoteHeaderObj)
        quoteHeaderJSON = JsonHelper.Deserialize(serializedQuote_data)
        return quoteHeaderJSON

    def GetCartItemData(self):
        url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{}/items'.format(self.quoteInfo.Id)
        encodedKeys = "Bearer " + str(self.bearer_token)
        headers = {"Authorization": encodedKeys}
        itemDataObj = RestClient.Get(url, headers)
        #serializedItem_data = JsonHelper.Serialize(itemDataObj)
        #quoteHeaderJSON = JsonHelper.Deserialize(serializedItem_data)
        #quoteHeaderJSON['ExternalConfiguration'] = itemConfig
        return itemDataObj
    
    def product_validation(self):
        quote = self.quoteInfo
        items = quote.GetAllItems()
        incomplete_products = []
        for item in items:
            if item['LBF_QU_PRODUCTSTATUS'] == 'Incomplete':
                incomplete_products.append(item.QuoteItem)
        return incomplete_products

    def run(self):
        incomplete_products = self.product_validation()
        if len(incomplete_products) == 0:
            self.bearer_token = self.GetBearerToken()
            if self.bearer_token == 'error':
                Log.Info("Error in retrieving bearer token.")
                return

            quoteheaderData = self.GetQuoteData()
            cpiEndUrl = (
                'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/CPQInboundQuote_SalesOrder'
            )  # awaiting from CPI team

            quoteitemData = self.GetCartItemData()
            
            sales_org_groups = {}

            data = list(quoteitemData)

            if data:

                # Iterate through each item
                for item in data:
                    # Find the LBF_QU_SalesOrg field
                    sales_org_value = None
                    for field in item["CustomFields"]:
                        if field["Name"] == "LBF_QU_SalesOrg":
                            sales_org_value = field["Content"]
                            sales_org_value = str(sales_org_value)
                            break

                    # Use the sales org value as the key in the dictionary
                    if sales_org_value not in sales_org_groups:
                        sales_org_groups[sales_org_value] = []
                    obj = JsonHelper.Deserialize(str(item))
                    sales_org_groups[sales_org_value].append(obj)

                # Display the grouped results
                for sales_org, items in sales_org_groups.items():
                    


                    requestData = {
                        'Root': {
                            "Quotes": quoteheaderData,
                            "Quoteitems": items
                        }
                    }
                    
                    json_obj = JsonHelper.Serialize(requestData)
                    Log.Info(str(json_obj))

                    Log.Info('MultiSales org requestData from CPQ to CPI ---->' + str(requestData))
                    try:
                        
                        cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, json_obj)
                    except Exception as e:
                        Log.Info('Error: Multi sales org as...: ' + str(e))
                        time.sleep(1)  # sleep 1 sec to send the payload as multiple times based on sales org type
        else:
            msg = "Please complete these products before placing order:\n"

            for item in incomplete_products:
                msg += "Item Number -  {0}\n".format(item)
            self.quoteInfo.AddMessage(msg, MessageLevel.Error, False)
            Log.Info(msg)


# Execute the process
MultiSalesOrg().run()
