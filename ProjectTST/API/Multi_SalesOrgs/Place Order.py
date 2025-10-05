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
            '''cpiEndUrl = (
                'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/CPQInboundQuote_SalesOrder'
            )'''
            cpiEndUrl = (
                'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/SIT2/CPQInboundQuote_SalesOrder'
            )

            quoteitemData = self.GetCartItemData()
            sales_org_groups = {}

            data = list(quoteitemData)

            if data:
                # Grouping items by sales organization
                for item in data:
                    sales_org_value = None
                    for field in item["CustomFields"]:
                        if field["Name"] == "LBF_QU_SalesOrg":
                            sales_org_value = field["Content"]
                            quoteheaderData["MarketCode"] = field["Content"]
                            sales_org_value = str(sales_org_value)
                            break

                    if sales_org_value not in sales_org_groups:
                        sales_org_groups[sales_org_value] = []
                    obj = JsonHelper.Deserialize(str(item))
                    sales_org_groups[sales_org_value].append(obj)

                # Processing each sales organization group
                for sales_org, items in sales_org_groups.items():
                    for field in items[0]["CustomFields"]:
                        if field["Name"] == "LBF_QU_SalesOrg":
                            quoteheaderData["MarketCode"] = field["Content"]
                        elif field["Name"] == "LBF_QU_DIV":
                            quoteheaderData["Division"] = field["Content"]
                        elif field["Name"] == "LBF_QU_DC":
                            quoteheaderData["DistributionChannel"] = field["Content"]

                    for index, item in enumerate(items, start=1):
                        #storing values
                        mat_cont = None
                        mat_value = None
                        frieght_cont = None
                        frieght_value = None
                        hand_cont = None
                        hand_value = None
                        sell_cont = None
                        sell_value = None
                        item_Number = item["ItemNumber"]
                        w_dat = []
                        for field in item['CustomFields']:
                            if field["Name"] == "LBF_QU_MAT_CST":
                                if field["Content"]:
                                    mat_cont = "ZPRS"
                                    mat_value = field["Content"]
                            elif field["Name"] == "LBF_QU_FREIGHT":
                                if field["Content"] == "QT":
                                    frieght_cont = "ZF01"
                            elif field["Name"] == "LBF_QU_FREIGHT_CST":
                                if field["Content"]:
                                    freight_value = field["Content"]
                            elif field["Name"] == "LBF_QU_HANDLING_CST":
                                if field["Content"]:
                                    hand_cont = "ZS01"
                                    hand_value = field["Content"]
                            elif field["Name"] == "LBF_QU_SELPRICE_UN":
                                if field["Content"]:
                                    sell_cont = "ZMAN"
                                    sell_value = field["Content"]
                        sell_dict = {
                                     "ITM_NUMBER": item_Number,
                                     "COND_TYPE" : sell_cont,
                                     "COND_VALUE": sell_value
                                     }
                        mat_dict = {
                                    "ITM_NUMBER": item_Number,
                                     "COND_TYPE" : mat_cont,
                                     "COND_VALUE": mat_value
                                    }
                        hand_dict = {
                                     "ITM_NUMBER": item_Number,
                                     "COND_TYPE" : hand_cont,
                                     "COND_VALUE": hand_value
                                     }
                        freight_dict = {
                                        "ITM_NUMBER": item_Number,
                                     "COND_TYPE" : frieght_cont,
                                     "COND_VALUE": frieght_value
                                        }
                        w_dat.append(sell_dict)
                        w_dat.append(mat_dict)
                        w_dat.append(hand_dict)
                        w_dat.append(freight_dict)
                        item["PricingData"] = w_dat

                    requestData = {
                        'Root': {
                            "Quotes": quoteheaderData,
                            "Quoteitems": items
                        }
                    }

                    json_obj = JsonHelper.Serialize(requestData)
                    Log.Info(str(json_obj))

                    try:
                        cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, json_obj)
                        Log.Info(str(cpiResponse))
                        time.sleep(1)
                    except Exception as e:
                        Log.Info('Error: Multi sales org process failed: ' + str(e))
                        time.sleep(1)
        else:
            msg = "Please complete these products before placing an order:\n"
            for item in incomplete_products:
                msg += "Item Number - {0}\n".format(item)
            self.quoteInfo.AddMessage(msg, MessageLevel.Error, False)
            Log.Info(msg)

# Execute the process
MultiSalesOrg().run()
