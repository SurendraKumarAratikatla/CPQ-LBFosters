import time
from LBF_GS_CREATEBEARERTOKEN import creating_bearer_token
from Scripting.Quote import MessageLevel

class MultiSalesOrg:
    def __init__(self, params):
        self.params = params
        self.quoteInfo = QuoteHelper.Get(context.Quote.QuoteNumber)
        self.bearer_token = ''
        self.headerStack = {}
        self.ItemStack = {}
        self.Root = {}

    # 🔹 Cleans smart quotes, dashes, and other non-ASCII symbols
    def clean_non_ascii(self, text):
        if text is None:
            return text
        try:
            if not isinstance(text, basestring):
                text = str(text)
            replacements = {
                u'“': '"', u'”': '"',
                u'‘': "'", u'’': "'",
                u'–': '-', u'—': '-',
                u'\xa0': ' ',  # non-breaking space
            }
            for bad, good in replacements.items():
                text = text.replace(bad, good)
            return ''.join([c if ord(c) < 128 else '?' for c in text])
        except Exception as e:
            return str(text)

    # 🔹 Converts .NET DateTime objects in dict/list structures to string
    def convert_datetime_to_str(self, data):
        import clr
        from System import DateTime
        if isinstance(data, dict):
            return {k: self.convert_datetime_to_str(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_datetime_to_str(v) for v in data]
        elif isinstance(data, DateTime):
            return data.ToString("yyyy-MM-ddTHH:mm:ssZ")
        else:
            return data

    def GetBearerToken(self):
        response = creating_bearer_token()
        if response[1] == 'success':
            stream = RestClient.DeserializeJson(StreamReader(response[0].GetResponseStream()).ReadToEnd())
            return stream.access_token
        else:
            return 'error'

    def deleteDupQuoteMsgs(self):
        spcount = 0
        shcount = 0
        spshcount = 0
        spMsg = "Please Enter Sold-to Party"
        shMsg = "Please Enter Ship-to Party"
        spshMsg = "Please enter Sold-to and Ship-to in Customer Info Tab"
        for msg in self.quoteInfo.Messages:
            if str(msg.Content) != str(spMsg):
                Trace.Write(msg.Content)
                spcount += 1
                return spcount
            elif str(msg.Content) != str(shMsg):
                Trace.Write(msg.Content)
                shcount += 1
                return shcount
            elif str(msg.Content) != str(spshMsg):
                Trace.Write(msg.Content)
                spshcount += 1
                return spshcount
        return 0

    def inv_party_check(self):
        involved_parties = context.Quote.GetInvolvedParties()
        ship_to = sold_to = None
        sh = sp = False
        for party in involved_parties:
            if party.PartnerFunctionName == "Ship-to party":
                ship_to = party.ExternalId
                sh = True
            elif party.PartnerFunctionName == "Sold-to party":
                sold_to = party.ExternalId
                sp = True
        if not sp and not sh:
            return "Please enter Sold-to and Ship-to in Customer Info Tab"
        elif not sp:
            return "Please Enter Sold-to Party"
        elif not sh:
            return "Please Enter Ship-to Party"
        if ship_to and sold_to:
            if not ship_to.strip() or not sold_to.strip():
                return ("Not a valid customer from S/4. "
                        "Please enter a valid Sold-to and Ship-to from S/4")
        return None

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

    def addAttributes(self, item_no):
        master = list()
        item = context.Quote.GetItemByItemNumber(item_no)
        prd = ProductHelper.CreateProduct(item.ProductId)
        attr = item.SelectedAttributes
        for a in attr:
            label = a.Name
            accss = prd.Attr(label).Access
            if str(accss) == "Editable":
                attr = prd.Attr(label).SystemId
                typ = prd.Attr(label).DisplayType
                values = a.Values
                for v in values:
                    temp = {
                        "CONFIG_ID": str(item_no).zfill(6),
                        "INST_ID": "00000001",
                        "CHARC": attr,
                        "VALUE": v.Display if typ == "FreeInputNoMatching" else v.ValueCode
                    }
                    Trace.Write(v.Display)
                    master.append(temp)
            elif str(accss) == "Hidden" and label == "Number of Lengths of Rail":
                attr_label = "Number of Lengths of Rail"
                temp = {
                    "CONFIG_ID": str(item_no).zfill(6),
                    "INST_ID": "00000001",
                    "CHARC": prd.Attr(attr_label).SystemId
                }
                typ = prd.Attr(attr_label).DisplayType
                for v in a.Values:
                    Log.Info(str(v.Display))
                    if typ == "FreeInputNoMatching":
                        code = v.Display
                        if int(str(code)):
                            temp["VALUE"] = code
                            master.append(temp)
        return master

    def checkVCItems(self, data):
        for item in data:
            partNumber = item["PartNumber"]
            Log.Info(str(partNumber))
            vcpPro = SqlHelper.GetList(
                "Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(
                    partNumber, 'True', 'False'))
            if vcpPro:
                item_no = item["ItemNumber"]
                segment_2 = self.addAttributes(item_no)
                item["E1BPCUVAL"] = segment_2
                item["E1BPCUCFG"] = {
                    "POSEX": item_no,
                    "CONFIG_ID": str(item_no).zfill(6),
                    "ROOT_ID": "00000001"
                }
        return data

    def updatePaymentTerms(self, customFields):
        for field in customFields:
            if field["Name"] == "LBF_CF_PAYTERMS" and "Content" in field:
                desc = field["Content"]
                query = "select Code, [Desc] from LBF_QU_PAYTERMS where [Desc] = '{0}'".format(desc)
                res = SqlHelper.GetFirst(query)
                if res:
                    code = res.Code
                    field["Content"] = str(code).zfill(4)
        return customFields

    def placeOrder(self):
        incomplete_products = self.product_validation()
        if len(incomplete_products) == 0:
            self.bearer_token = self.GetBearerToken()
            if self.bearer_token == 'error':
                return
            quoteheaderData = self.GetQuoteData()
            quoteheaderData["CustomFields"] = self.updatePaymentTerms(quoteheaderData["CustomFields"])
            cpiEndUrl = (
                'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/SIT2/CPQInboundQuote_SalesOrder'
            )
            quoteitemData = self.GetCartItemData()
            data = list(quoteitemData)

            if self.inv_party_check() != None:
                msg = self.inv_party_check()
                if self.deleteDupQuoteMsgs() == 0:
                    self.quoteInfo.AddMessage(msg, MessageLevel.Error, False)
                return

            if data:
                updated_items = []
                for d in data:
                    for cust in d["CustomFields"]:
                        if cust["Name"] == "LBF_QU_SO_STATUS" and cust["Content"] != "Invalid S/4 Material":
                            updated_items.append(d)

                sales_org_groups = {}
                for item in updated_items:
                    sales_org_value = None
                    for field in item["CustomFields"]:
                        if field["Name"] == "LBF_QU_SalesOrg":
                            sales_org_value = str(field["Content"])
                            quoteheaderData["MarketCode"] = field["Content"]
                            break
                    if sales_org_value not in sales_org_groups:
                        sales_org_groups[sales_org_value] = []
                    obj = JsonHelper.Deserialize(self.clean_non_ascii(str(item)))
                    sales_org_groups[sales_org_value].append(obj)

                for sales_org, items in sales_org_groups.items():
                    updated_items = self.checkVCItems(items)
                    sales_org_groups[sales_org] = updated_items

                for sales_org, items in sales_org_groups.items():
                    requestData = {
                        'Root': {
                            "Quotes": quoteheaderData,
                            "Quoteitems": items
                        }
                    }

                    # ✅ Clean and convert data before JSON serialization
                    cleaned_data = self.convert_datetime_to_str(requestData)
                    cleaned_data = self.clean_non_ascii(cleaned_data)
                    json_obj = JsonHelper.Serialize(cleaned_data)

                    Log.Info(self.clean_non_ascii(json_obj))
                    try:
                        cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, json_obj)
                        Log.Info(self.clean_non_ascii(str(cpiResponse)))
                        time.sleep(1)
                    except Exception as e:
                        Log.Info('Error: Multi sales org process failed: ' + str(e))
                        time.sleep(1)

                for item in context.Quote.GetAllItems():
                    if item.AsMainItem and item["LBF_QU_SO_STATUS"] == "":
                        if item["LBF_QU_SO_STATUS"] != "Invalid S/4 Material":
                            item["LBF_QU_SO_STATUS"] = "Order Confirmation Pending"
        else:
            msg = "Please complete these products before placing an order:\n"
            for item in incomplete_products:
                msg += "Item Number - {0}\n".format(item)
            self.quoteInfo.AddMessage(msg, MessageLevel.Error, False)

    def itemsSyncCheck(self):
        items = ""
        count = 0
        item_status = []
        for item in self.quoteInfo.GetAllItems():
            if item['LBF_QU_SO_STATUS'] != "" and item['LBF_QU_SO_STATUS'] not in item_status:
                item_status.append(item['LBF_QU_SO_STATUS'])
                continue
        if 'Order Confirmation Pending' in item_status:
            return "Order confirmation pending. Please wait a moment."
        elif item_status != []:
            return 'Order is already placed for the quote. Refresh the page to update Header status.'
        for item in self.quoteInfo.GetAllItems():
            lastItemId = item.RolledUpQuoteItem
            partNumber = item.PartNumber
            proSync = SqlHelper.GetList(
                "Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}'".format(
                    partNumber, 'True'))
            if not proSync:
                if items:
                    items = str(items) + ","
                items = items + str(item.RolledUpQuoteItem)
                item['LBF_QU_SO_STATUS'] = "Invalid S/4 Material"
        if items:
            return items
        else:
            customFields = ""
            poDate = context.Quote.GetCustomField("LBF_CF_PODATE").Value
            inco1 = context.Quote.GetCustomField("LBF_CF_INCOTERMS").Value
            inco2 = context.Quote.GetCustomField("LBF_CF_INCOTERMS2").Value
            payTerms = context.Quote.GetCustomField("LBF_CF_PAYTERMS").Value
            poNumber = context.Quote.GetCustomField("LBF_CF_PONUMBER").Value

            if poDate == '' or poDate == '0':
                customFields += "PO Date, "
            if inco1 == '0' or inco1 == '':
                customFields += "incoterms, "
            if inco2 == '' or inco2 == '0':
                customFields += "incoterms1, "
            if payTerms == '0' or payTerms == '':
                customFields += "Payment Terms, "
            if poNumber == '' or poNumber == '0':
                customFields += "PO Number, "
            if customFields:
                return "Please enter the " + str(customFields)[:-2] + " values before placing the order."
            else:
                return ""

    def run(self):
        if self.params.Action == "itemsSyncCheck":
            return self.itemsSyncCheck()
        elif self.params.Action == "orderProcessing":
            self.placeOrder()
            return True

response_data = MultiSalesOrg(Param).run()
ApiResponse = ApiResponseFactory.JsonResponse(response_data)
