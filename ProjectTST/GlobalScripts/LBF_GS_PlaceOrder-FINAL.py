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
    def addAttributes(self,item_no):
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
                    if typ == "FreeInputNoMatching":
                        temp = {}
                        temp["CONFIG_ID"] = str(item_no).zfill(6)
                        temp["INST_ID"] = "00000001"
                        temp["CHARC"] = attr
                        code = v.Display
                        temp["VALUE"] = code
                        Trace.Write(code)
                        master.append(temp)
                    else:
                        temp = {}
                        temp["CONFIG_ID"] = str(item_no).zfill(6)
                        temp["INST_ID"] = "00000001"
                        temp["CHARC"] = attr
                        code = v.ValueCode
                        temp["VALUE"] = code
                        Trace.Write(code)
                        master.append(temp)
            elif str(accss) == "Hidden" and label == "Number of Lengths of Rail":
                #Log.Info(str(label))
                attr_label = "Number of Lengths of Rail"
                temp = {}
                attr = prd.Attr(attr_label).SystemId
                typ = prd.Attr(attr_label).DisplayType
                temp["CONFIG_ID"] = str(item_no).zfill(6)
                temp["INST_ID"] = "00000001"
                temp["CHARC"] = attr
                values = a.Values
                for v in values:
                    Log.Info(str(v.Display))
                    if typ == "FreeInputNoMatching":
                        code = v.Display
                        if int(str(code)):
                            temp["VALUE"] = code
                            Trace.Write(code)
                            Log.Info("rail number")
                            Log.Info(str(code))
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
                         "CONFIG_ID" : str(item_no).zfill(6),
                         "ROOT_ID" : "00000001"
                                     }
                Log.Info(str(temp))
                item["E1BPCUCFG"] = temp
                #Log.Info(str(item))
        return data
    
    def updatePaymentTerms(self, customFields):
        for field in customFields:
            if field["Name"] == "LBF_CF_PAYTERMS":
                if "Content" in field:
                    desc = field["Content"]
                    query = "select Code, [Desc] from LBF_QU_PAYTERMS where [Desc] = '{0}'".format(desc)
                    res = SqlHelper.GetFirst(query)
                    if res:
                        code = res.Code
                        paddedCode = str(code).zfill(4)
                        field["Content"] = paddedCode
        return customFields
                

    def placeOrder(self):
        incomplete_products = self.product_validation()
        if len(incomplete_products) == 0:
            self.bearer_token = self.GetBearerToken()
            if self.bearer_token == 'error':
                #Log.Info("Error in retrieving bearer token.")
                return

            quoteheaderData = self.GetQuoteData()
            
            customFields = quoteheaderData["CustomFields"]
            updatedcustomFields = self.updatePaymentTerms(customFields)
            quoteheaderData["CustomFields"] = updatedcustomFields
            
            '''cpiEndUrl = (
                'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/CPQInboundQuote_SalesOrder'
            )'''
            cpiEndUrl = (
                'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/SIT2/CPQInboundQuote_SalesOrder'
            )

            quoteitemData = self.GetCartItemData()
            sales_org_groups = {}

            data = list(quoteitemData)
            
            #checking for involved party
            inv_party = context.Quote.GetInvolvedParties()
            count = sum(1 for _ in inv_party) if inv_party else 0
            
            if self.inv_party_check() != None:
                msg = self.inv_party_check()
                if self.deleteDupQuoteMsgs() == 0:
                    self.quoteInfo.AddMessage(msg, MessageLevel.Error, False)

            elif data:
                updated_items = []
                for d in data:
                    #Log.Info(str(d))
                    for cust in d["CustomFields"]:
                        if cust["Name"] == "LBF_QU_SO_STATUS" and cust["Content"] != "Invalid S/4 Material":
                            updated_items.append(d)
                # Grouping items by sales organization
                for item in updated_items:
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
                    # Log.Info("sales_org--->"+str(sales_org))
                    # Log.Info("updated_items--->"+str(updated_items))
                    sales_org_groups[sales_org] = updated_items

                    # # Processing each sales organization group
                    # Log.Info("sales_org_groups[sales_org]--->"+str(sales_org_groups[sales_org]))
                    # for sales_org, items in sales_org_groups.items():
                    for field in items[0]["CustomFields"]:
                        if field["Name"] == "LBF_QU_SalesOrg":
                            quoteheaderData["MarketCode"] = field["Content"]
                        elif field["Name"] == "LBF_QU_DIV":
                            quoteheaderData["Division"] = field["Content"]
                        elif field["Name"] == "LBF_QU_DC":
                            quoteheaderData["DistributionChannel"] = field["Content"]

                    for index, item in enumerate(items, start=1):
                        #changing value in taruom
                        marketCode = quoteheaderData["MarketCode"]
                        #Log.Info(str(marketCode))
                        #Log.Info(str(item))
                        if str(marketCode) == "3131" and item["PartNumber"] == "6981000":
                            conditionlist = []
                            engineer_value = None
                            freight_fb = None
                            price = item["PricingDetails"]["Fixed"]["ListPrice"]["Value"]
                            cost = item["PricingDetails"]["Fixed"]["Cost"]["Value"]
                            #Log.Info(str(cost))
                            #Log.Info(str(price))
                            cost = {
                            "ITM_NUMBER": item["ItemNumber"],
                                     "COND_TYPE" : "ZPRS",
                                     "COND_VALUE": cost
                            }
                            price = {
                            "ITM_NUMBER": item["ItemNumber"],
                                     "COND_TYPE" : "PR00",
                                     "COND_VALUE": price
                            }
                            cust_field = item["CustomFields"]
                            for f in cust_field:
                                if f["Name"] == "LBF_QU_Engineering":
                                    if f["Content"]:
                                        engineer_value = f["Content"]
                                elif f["Name"] == "LBF_QU_FreightFB":
                                    if f["Content"]:
                                        freight_fb = f["Content"]
                            freight_dict_infra = {
                            "ITM_NUMBER": item["ItemNumber"],
                                     "COND_TYPE" : "ZMSC",
                                     "COND_VALUE": engineer_value
                            }
                            engineering_dict_infra = {
                                "ITM_NUMBER": item["ItemNumber"],
                                     "COND_TYPE" : "ZF02",
                                     "COND_VALUE": freight_fb
                            }
                            conditionlist.append(freight_dict_infra)
                            conditionlist.append(engineering_dict_infra)
                            conditionlist.append(cost)
                            conditionlist.append(price)
                            item["PricingData"] = conditionlist
                            #Log.Info(str(conditionlist[0]))
                            #Log.Info(str(conditionlist[1]))
                        for f in item["CustomFields"]:
                            if f["Name"] == "LBF_QU_TARUOM" and f["Content"] == "FT":
                                f["Content"] = "FT"
                        #changing unit of measure values
                        if item["UnitOfMeasure"] == "FT":
                            item["UnitOfMeasure"] = "FT"
                        elif item["UnitOfMeasure"] == "LB":
                            item["UnitOfMeasure"] = "LB"
                        partNumber = item["PartNumber"]
                        #vcpProCheck = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(partNumber,'True','False'))
                        listPriceCheck = next(item['Content'] for item in item['CustomFields'] if item.get('Name') == 'LBF_QU_CXT_SMPVCP')
                        #storing values
                        mat_cont = None
                        mat_value = None
                        frieght_cont = None
                        frieght_value = None
                        hand_cont = None
                        hand_value = None
                        sell_cont = None
                        sell_value = None
                        rail_cont = None
                        rail_value = None
                        item_Number = item["ItemNumber"]
                        w_dat = []
                        Log.Info("item['CustomFields']--->"+str(item['CustomFields']))
                        for field in item['CustomFields']:
                            # plant LBF_QU_PLANT1
                            if field["Name"] == "LBF_QU_PLANT1":
                                plant1 = field["Content"]
                            #payment terms
                            if field["Name"] == "LBF_CF_PAYTERMS":
                                if field["Content"]:
                                    paystr = field["Content"]
                                    query = "select Code, Desc from LBF_QU_PAYTERMS where Desc = '{0}'".format(paystr)
                                    res = SqlHelper.GetFirst(query)
                                    code = res.Code
                            
                            # Validations on LBF_QU_CONDMAP custom table to get customfield Condition types
                            query_condmap_data = SqlHelper.GetList("select SORG, CustomField, Variation, ConditionType from LBF_QU_CONDMAP where SORG='{0}' and CustomField='{1}'".format(sales_org,field["Name"]))
                            if query_condmap_data:
                                for row in query_condmap_data:
                                    if str(row.CustomField) == "LBF_QU_MAT_CST_OVR":
                                        if field["Content"] and int(float(field["Content"])) !=0:
                                            mat_cont = str(row.ConditionType)
                                            mat_value = field["Content"]
                                    elif str(row.CustomField) == "LBF_QU_FREIGHT":
                                        if field["Content"] == "QT" and str(row.Variation) == "QT":
                                            frieght_cont = str(row.ConditionType)
                                        elif field["Content"] == "WT" and str(row.Variation) == "WT":
                                            frieght_cont = str(row.ConditionType)
                                        elif (field["Content"] == "FC" or field["Content"] == "FIX") and (str(row.Variation) == "FC" or str(row.Variation) == "FIX"):
                                            frieght_cont = str(row.ConditionType)
                                    elif str(row.CustomField) == "LBF_QU_FREIGHT_CST":
                                        #if str(field["Content"]) == str(row.Variation):
                                        if field["Content"]:
                                            frieght_value = field["Content"]
                                    elif str(row.CustomField) == "LBF_QU_HANDLING_OB":
                                        if field["Content"] == "QT" and str(row.Variation) == "QT":
                                            hand_cont = str(row.ConditionType)
                                        elif field["Content"] == "MIN" and str(row.Variation) == "MIN":
                                            hand_cont = str(row.ConditionType)                                            
                                    elif str(row.CustomField) == "LBF_QU_HANDLING_CST":
                                        if field["Content"]:
                                            #hand_cont = str(row.ConditionType)
                                            hand_value = field["Content"]
                                    elif str(row.CustomField) == "LBF_QU_SELPRICE_UN" and listPriceCheck != "Simple": #(field["Name"] == "LBF_QU_CXT_SMPVCP" and field["Content"] != "Simple")
                                        if field["Content"]:
                                            sell_cont = str(row.ConditionType)
                                            sell_value = field["Content"]
                                    elif str(row.CustomField) == "LBF_QU_RAIL_USPR" or str(row.CustomField) == "LBF_QU_RAIL_TRNRNT":
                                        if field["Content"]:
                                            rail_cont = str(row.ConditionType)
                                            rail_value = field["Content"]
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
                        rail_dict = {
                                     "ITM_NUMBER": item_Number,
                                     "COND_TYPE" : rail_cont,
                                     "COND_VALUE": rail_value
                        }
                        if str(marketCode) != "3131":
                            w_dat.append(sell_dict)
                            w_dat.append(rail_dict)
                            vcpPro = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(partNumber,'True','False'))
                            if len(vcpPro) == 0:
                                w_dat.append(mat_dict)
                            # validation for Handling cost 
                            query_handling_cost = SqlHelper.GetList("select PLANT, QTY, MIN from LBF_QU_HAND_COST where PLANT='{0}'".format(plant1))
                            if query_handling_cost:
                                for row in query_handling_cost:
                                    if hand_value:
                                        if float(hand_value) != max(float(row.QTY),float(row.MIN)) and float(hand_value) > 0:
                                            w_dat.append(hand_dict)
                            w_dat.append(freight_dict)
                            item["PricingData"] = w_dat
                        Log.Info(str(item))

                    # ascii validation
                    Log.Info("sales_org--->"+str(sales_org))
                    Log.Info("updated_items--->"+str(updated_items))
                    deser_data = JsonHelper.Deserialize(JsonHelper.Serialize(updated_items))
                    #Trace.Write(deser_data[0]['CustomFields'])
                    for row in deser_data[0]['CustomFields']:
                        if row['Name'] == "LBF_QU_Notes" or row['Name'] == "LBF_QU_ITEMDESC":
                            row['Content'] = row['Content'].replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace("–","–").replace("—","—")
                            #Trace.Write(row['Content'])

                    requestData = {
                        'Root': {
                            "Quotes": JsonHelper.Deserialize(JsonHelper.Serialize(quoteheaderData)),
                            "Quoteitems": deser_data
                        }
                    }

                    #json_obj = JsonHelper.Deserialize(JsonHelper.Serialize(str(requestData).replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace("–","–").replace("—","—")))
                    #json_obj = JsonHelper.Serialize(requestData)
                    Log.Info("deser_data---->"+str(deser_data))

                    try:
                        cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, requestData)
                        Log.Info(str(cpiResponse))
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
            #Log.Info(msg)

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
            proSync = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}'".format(partNumber,'True'))
            if not proSync:
                if items:
                    items = str(items) + ","
                items = items + str(item.RolledUpQuoteItem)
                item['LBF_QU_SO_STATUS'] = "Invalid S/4 Material"
        #Log.Info("itemsSyncCheck--->items: "+str(items))
        if items:
            return items
        else:
            customFields = ""
            poDate = context.Quote.GetCustomField("LBF_CF_PODATE").Value # LBF_CF_PODATE
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
                return "Please enter the "+str(customFields)[:-2]+" values before placing the order."
            else:
                return ""


    def run(self):
        if self.params.Action == "itemsSyncCheck":
            return self.itemsSyncCheck()
        
        elif self.params.Action == "orderProcessing":
            # Execute the process
            self.placeOrder()
            return True

response_data = MultiSalesOrg(Param).run()
ApiResponse = ApiResponseFactory.JsonResponse(response_data)