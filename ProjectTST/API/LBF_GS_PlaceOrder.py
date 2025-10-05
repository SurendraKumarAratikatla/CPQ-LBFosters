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
                #self.quoteInfo.AddMessage(str(spMsg), MessageLevel.Error, False)
                return spcount
            elif str(msg.Content) != str(shMsg):
                Trace.Write(msg.Content)
                shcount += 1
                #self.quoteInfo.AddMessage(str(shMsg), MessageLevel.Error, False)
                return shcount
            elif str(msg.Content) != str(spshMsg):
                Trace.Write(msg.Content)
                spshcount += 1
                #self.quoteInfo.AddMessage(str(spshMsg), MessageLevel.Error, False)
                return spshcount
        return 0

    def inv_party_check(self):
        involved_parties = context.Quote.GetInvolvedParties()
        # if not involved_parties:
        #     return "Please enter Sold-to and Ship-to in Customer Info Tab"

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
    def addAttributes(self,item_no):
        master = list()
        item = context.Quote.GetItemByItemNumber(item_no)
        prd = ProductHelper.CreateProduct(item.ProductId)
        attr = item.SelectedAttributes
        for a in attr:
            label = a.Name
            accss = prd.Attr(label).Access
            if str(accss) == "Editable":
                temp = {}
                attr = prd.Attr(label).SystemId
                typ = prd.Attr(label).DisplayType
                temp["CONFIG_ID"] = "000001"
                temp["INST_ID"] = "00000001"
                temp["CHARC"] = attr
                values = a.Values
                for v in values:
                    code = v.ValueCode
                    temp["VALUE"] = code
            	master.append(temp)
        return master
    
    def checkVCItems(self, data):
        for item in data:
            partNumber = item["PartNumber"]
            Log.Info(str(partNumber))
            vcpPro = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(partNumber,'True','False'))
            if vcpPro:
                item_no = item["ItemNumber"]
                segment_2 = self.addAttributes(item_no)
                item["E1BPCUVAL"] = segment_2
                temp = {
                         "POSEX" : item_no,
                         "CONFIG_ID" : "000001",
                         "ROOT_ID" : "00000001"
                                     }
                item["E1BPCUCFG"] = temp
                Log.Info(str(item))
        return data

    def placeOrder(self):
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


            for item in data:

                for cust in item["CustomFields"]:
                    if cust["Name"] == "LBF_QU_SO_STATUS" and cust["Content"] == "Order Confirmation Pending":
                        data.Remove(item)            
                        
            #checking for involved party
            inv_party = context.Quote.GetInvolvedParties()
            count = sum(1 for _ in inv_party) if inv_party else 0
            
            if self.inv_party_check() != None:
                msg = self.inv_party_check()
                if self.deleteDupQuoteMsgs() == 0:
                    self.quoteInfo.AddMessage(msg, MessageLevel.Error, False)

            elif data:
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
                    
                #checking item is vc or not
                for sales_org, items in sales_org_groups.items():
                    updated_items = self.checkVCItems(items)
                    sales_org_groups[sales_org] = updated_items

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
                        #changing value in taruom
                        for f in item["CustomFields"]:
                            if f["Name"] == "LBF_QU_TARUOM" and f["Content"] == "FOT":
                                f["Content"] = "FT"
                        #changing unit of measure values
                        if item["UnitOfMeasure"] == "FOT":
                            item["UnitOfMeasure"] = "FT"
                        elif item["UnitOfMeasure"] == "LBR":
                            item["UnitOfMeasure"] = "LB"
                        partNumber = item["PartNumber"]
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
                        vcpPro = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(partNumber,'True','False'))
                        if len(vcpPro) == 0:
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
                for item in context.Quote.GetAllItems():
                    if item.AsMainItem:
                        item["LBF_QU_SO_STATUS"] = "Order Confirmation Pending"
        else:
            msg = "Please complete these products before placing an order:\n"
            for item in incomplete_products:
                msg += "Item Number - {0}\n".format(item)
            self.quoteInfo.AddMessage(msg, MessageLevel.Error, False)
            Log.Info(msg)

    def itemsSyncCheck(self):
        items = ""
        count = 0
        for item in self.quoteInfo.GetAllItems():
            lastItemId = item.RolledUpQuoteItem
            partNumber = item.PartNumber
            proSync = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}'".format(partNumber,'True'))
            if not proSync:
                if items:
                    items = str(items) + ","
                items = items + str(item.RolledUpQuoteItem)
        Log.Info("itemsSyncCheck--->items: "+str(items))
        return items

    def run(self):
        if self.params.Action == "itemsSyncCheck":
            return self.itemsSyncCheck()
        
        elif self.params.Action == "orderProcessing":
            # Execute the process
            self.placeOrder()
            return True

response_data = MultiSalesOrg(Param).run()
ApiResponse = ApiResponseFactory.JsonResponse(response_data)