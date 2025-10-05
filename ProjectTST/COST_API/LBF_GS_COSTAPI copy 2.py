class CostAPI:
    def __init__(self, context):
        self.context = context
        self.Product = context.Product
        self.marketId = context.Quote.MarketId
        self.attrStack = ""
        self.keys = ''
        self.values = ''
        self.dictStack = {}
        self.currentItemId = 0
        self.plant = ''
        self.disCha = ''
        self.division = ''
        self.errMsg = ''
        self.payload = {
            'ORDER_HEADER_IN': {
                'DOC_TYPE': 'ZSIM',
                'SALES_ORG': '4200',
                'DISTR_CHAN': '10',
                'DIVISION': '40',
                'PURCH_NO': ''
            },
            'ORDER_ITEMS_IN': {
                'ITM_NUMBER': '000001',
                'PO_ITM_NO': '1',
                'MATERIAL': '',
                'TARGET_QTY': '1',
                'PLANT' : '',
            },
            'ORDER_PARTNERS': {},
            'ORDER_SCHEDULE_IN': {
                'ITM_NUMBER': '000001',
                'SCHED_LINE': '0001',
                'REQ_QTY': '1'
            },
            'ORDER_CFGS_REF': {
                'POSEX': '',
                'CONFIG_ID': '000001',
                'ROOT_ID': '00000001',
                'SCE': '1',
                'COMPLETE': 'T',
                'CONSISTENT': 'T',
            },
            'ORDER_CFGS_INST': {
                'CONFIG_ID': '000001',
                'INST_ID': '00000001',
                'OBJ_TYPE': 'MARA',
                'CLASS_TYPE': '300',
                'OBJ_KEY': '',
                'QUANTITY': '1',
            },
            'ORDER_CFGS_VALUE': []
        }

    def accessMatCostTbl(self,prtNo):
        # prtNo = self.Product.PartNumber
        data = SqlHelper.GetFirst("SELECT * from LBF_QU_MAT_COST WHERE MATERIAL = '{0}' ".format(prtNo))
        if data:
            # if str(self.marketId) != "8" and str(self.marketId) != "7":
            currentPlant = data.Plant
            # Log.Info("currentPlant:--->"+str(currentPlant))
            self.plant = str(currentPlant)
            self.salesOrg = data.SORG
            self.disCha = data.DC
            self.division = data.DIV
        
        else:
            self.plant = ''
            self.salesOrg = ''
            self.disCha = ''
            self.division = ''
        

    def getRolledupItemId(self):
        self.currentItemId = 0
        #Log.Info('self.currentItemId-- Out-->'+str(self.currentItemId))
        for item in context.Quote.GetAllItems():
            self.currentItemId += 1
            #Log.Info('self.currentItemId-- In-->'+str(self.currentItemId))

    def getCostErrorMsgs(self,resErrorMsgArr):
        resErrorMsg = JsonHelper.Deserialize(str(resErrorMsgArr))
        if str(type(resErrorMsg)) == "<type 'list'>":
            for item in resErrorMsg:
                #Log.Info(item['TYPE'])
                #if str(item['TYPE']) == "E":
                self.errMsg += str(item['MESSAGE']) + '. '
                #Log.Info(item['MESSAGE'])
            pass

        elif str(type(resErrorMsg)) == "<type 'list'>":
            #if str(resErrorMsg['TYPE']) == "E":
            self.errMsg += str(item['MESSAGE']) + '. '

    def update_header(self):

        """Update header information based on the quote."""
        for item in context.Quote.GetAllItems():
            Log.Info("item.PartNumber: item.RolledUpQuoteItem---> "+str(item.RolledUpQuoteItem))
            Log.Info("item.PartNumber: self.currentItemId---> "+str(self.currentItemId))

            if str(int(item.RolledUpQuoteItem)) == str(int(self.currentItemId)):
                Log.Info("item.PartNumber:---> "+str(item.PartNumber))
                self.accessMatCostTbl(item.PartNumber)
                self.payload['ORDER_HEADER_IN']['PURCH_NO'] = self.context.Quote.QuoteNumber
                self.payload['ORDER_ITEMS_IN']['MATERIAL'] = item.PartNumber
                self.payload['ORDER_ITEMS_IN']['PLANT'] = self.plant
                self.payload['ORDER_ITEMS_IN']['PO_ITM_NO'] = str(self.currentItemId)
                self.payload['ORDER_CFGS_INST']['OBJ_KEY'] = self.Product.PartNumber
                #Log.Info('self.currentItemId-- AT-->'+str(self.currentItemId))
                self.payload['ORDER_CFGS_REF']['POSEX'] = "00000"+str(self.currentItemId)

                self.payload['ORDER_HEADER_IN']['SALES_ORG'] = self.salesOrg
                self.payload['ORDER_HEADER_IN']['DISTR_CHAN'] = self.disCha
                self.payload['ORDER_HEADER_IN']['DIVISION'] = self.division
                break

    def update_partners(self):
        """Update partner information in the payload."""
        involved_parties = self.context.Quote.GetInvolvedParties()
        for party in involved_parties:
            self.payload['ORDER_PARTNERS'][party.PartnerFunctionKey] = {
                'PARTN_ROLE': party.PartnerFunctionKey,
                'PARTN_NUMB': party.ExternalId
            }

    def beautifyAttrStr(self):
        # longest_attr = max(self.dictStack.keys(), key=len)
        # longest_attr_length = len(longest_attr)
        # self.attrStack = "\n".join("{} : {}".format(key.ljust(longest_attr_length)+"     ", "  "+str(value)) for key, value in self.dictStack.items())
        self.keys = "\n".join("{}".format(key) for key in self.dictStack.keys())
        self.values =  "\n".join(": {}".format(value) for value in self.dictStack.values())


    def populate_cfgs_value(self):
        """Populate ORDER_CFGS_VALUE with editable attributes."""
        tot_attr = self.Product.Attributes
        #editable_attr = [attr.Name for attr in tot_attr if str(attr.Access) == 'Editable']
        for item in tot_attr:
            count = 0
            system_id = item.SystemId
            attrName = item.Name
            values = item.Values
            for value in values:
                if value.IsSelected == True:
                    count += 1
                    valueCode = str(value.ValueCode)
                    #value = str(value.UserInput) if valueCode == "DefaultValue" else valueCode
                    
                    if str(self.marketId) != "8" and str(self.marketId) != "7":
                        targetQtyUOM = self.Product.Attr('Target quantity UoM').GetValue()
                    else:
                        targetQtyUOM = ""
                    #if attrName == "Target quantity UoM" and value != "EA":
                    if attrName == "Number of Lengths of Rail" and targetQtyUOM != "EA":
                        isShortsAllowed = self.Product.Attr('Shorts allowed?').GetValue()
                        if isShortsAllowed != "Yes - Shorts Allowed":
                            calQtyUOM = self.Product.Attr('Calculated Quantity for UOM').GetValue()
                            overalLen = self.Product.Attr('Overall Length (TOTAL IN)').GetValue()
                            value = (float(calQtyUOM) * 12) / float(overalLen)
                            Log.Info("UOM: NOT EA Calculations if Value: "+str(value))
                            break

                        elif isShortsAllowed == "Yes - Shorts Allowed":
                            calQtyUOM = self.Product.Attr('Calculated Quantity for UOM').GetValue()
                            perShortsAllow = self.Product.Attr('Percentage of Shorts Allowed').GetValue()
                            overalLen = self.Product.Attr('Overall Length (TOTAL IN)').GetValue()
                            assShortsLen = self.Product.Attr('Assumed Shorts Length').GetValue()
                            value = (float(calQtyUOM) * 12 * (1 - (float(perShortsAllow) / 100)) / float(overalLen) ) + ((float(calQtyUOM) * (float(perShortsAllow)/100) * 12) / (float(assShortsLen) * 12))
                            Log.Info("UOM: NOT EA Calculations elif Value: "+str(value))
                            break
                        else:
                            value = ""
                            Log.Info("UOM: NOT EA Calculations else Value: "+str(value))
                            break
                    else:
                        if str(system_id) == "OA_LENGTH_FT" or str(system_id) == "OA_LENGTH_IN":
                            value = value.UserInput
                            break
                        else:
                            value = str(value.UserInput) if valueCode == "DefaultValue" else valueCode
                            break
            if count == 0:
                value = ""
            if str(item.Access) != 'Hidden':
                self.dictStack[attrName] = value

            self.payload['ORDER_CFGS_VALUE'].append({
                    'CONFIG_ID': '000001',
                    'INST_ID': '00000001',
                    'CHARC': system_id,
                    'VALUE': value
                })

    def responseUpdateAtCart(self,resMatCost,resErrorMsg):
        # Error msg
        #Log.Info('resErrorMsg---'+str(resErrorMsg))
        #Log.Info("TYPE: resErrorMsg----"+str(type(resErrorMsg)))
        self.getCostErrorMsgs(resErrorMsg)
        Log.Info("self.errMsg----"+str(self.errMsg))
        Log.Info('COST API Response COST if-->'+str(resMatCost))
        for item in context.Quote.GetAllItems():
            if str(int(item.RolledUpQuoteItem)) == str(int(self.currentItemId)):
                Log.Info('COST API Response COST elif-->'+str(resMatCost))
                item['LBF_QU_ITEMCONFIG'] = str(self.keys)
                item['LBF_QU_ITEMCONFIG1'] = str(self.values)
                if self.errMsg != '':
                    Log.Info('innnnn if')
                    item['LBF_QU_MAT_CST'] = str(resMatCost)
                    item['LBF_QU_COSTSTATUS'] = "Error"
                    item['LBF_QU_COSTERROR'] = str(self.errMsg)
                    break
                elif self.errMsg == '' and resMatCost != '':
                    Log.Info('innnnn elif 1')
                    item['LBF_QU_MAT_CST'] = str(resMatCost)
                    item['LBF_QU_COSTSTATUS'] = "Success"
                    item['LBF_QU_COSTERROR'] = 'Cost is added to the line item.'
                    break
                elif self.errMsg == '' and resMatCost == '':
                    Log.Info('innnnn elif 2')
                    item['LBF_QU_MAT_CST'] = str(resMatCost)
                    item['LBF_QU_COSTSTATUS'] = "Error Warning"
                    item['LBF_QU_COSTERROR'] = 'Cost data is not retrieved from S4 - Please contact Administrator'
                    break

    def UOMQtyUpdate(self):
        for item in context.Quote.GetAllItems():
            Log.Info('LBF_QU_TARUOM-->'+str(item['LBF_QU_TARUOM']))
            Log.Info('item.RolledUpQuoteItem-->'+str(item.RolledUpQuoteItem))
            Log.Info('int(self.currentItemId)-->'+str(int(self.currentItemId)))
            if str(int(item.RolledUpQuoteItem)) == str(int(self.currentItemId)) and str(item['LBF_QU_TARUOM']) != 'FOT':
                alterUOM = str(item['LBF_QU_TARUOM'])
                # if str(self.marketId) != "8" and str(self.marketId) != "7":
                try:
                    #UOMdata = SqlHelper.GetFirst("Select * from LBF_QU_UOM_CONV_RATES where Material ='{0}' and TargetUOM='{1}'".format(str(self.Product.PartNumber), str(alterUOM)))
                    Numerator_Fact_Conv = self.Product.Attr('Numerator (factor) for convers').GetValue()
                    Denominator_Fact_Conv = self.Product.Attr('Denominator (Divisor) for Conv').GetValue()
                    cumQty = self.Product.Attr('Cumulative Order Quantity in S').GetValue()

                    if Numerator_Fact_Conv:
                        Denominator_Fact_Conv = 1 if not Denominator_Fact_Conv else Denominator_Fact_Conv
                        convFactor = float(Numerator_Fact_Conv) / float(Denominator_Fact_Conv)
                        self.payload['ORDER_ITEMS_IN']['TARGET_QTY'] = str(round(float(float(item.Quantity) * float(convFactor)),3))
                        self.payload['ORDER_SCHEDULE_IN']['REQ_QTY'] = str(round(float(float(cumQty) * float(convFactor)),3))
                        Log.Info('UOM:QUANTITY-->'+str(self.payload['ORDER_CFGS_INST']['QUANTITY']))
                        break
                except Exception as e:
                    Log.Info('Error Ignore: In Numerator and Denominator not present as :'+str(e))
        return

    # deleting all quote messages
    def delete_quote_msgs(self):
        for msg in context.Quote.Messages:
            context.Quote.DeleteMessage(msg.Id)

    def process(self):
        """Main process to update the payload."""
        self.getRolledupItemId()
        # self.accessMatCostTbl()
        self.update_header()
        self.update_partners()
        self.populate_cfgs_value()
        Log.Info("self.dictStack:----->"+str(self.dictStack)) # self.attrStack
        # Log.Info("self.attrStack:----->"+str(self.attrStack)) # self.attrStack
        self.beautifyAttrStr()
        self.UOMQtyUpdate()
        Log.Info("Final Payload:")
        #Log.Info(str(self.payload))
        data = JsonHelper.Serialize(self.payload)
        Log.Info("CPQ Request Payload: "+str(data))
        # S4D URL
        #cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/Replicate_Cost_to_S4'
        # S4Q URL
        cpiEndUrl = "https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/SIT2/Replicate_Cost_to_S4"
        try:
            cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, data)
            Log.Info("S4 Response Payload: "+str(cpiResponse))
            resMatCost = cpiResponse['ns0:SD_SALESDOCUMENT_CREATEResponse']['CONDITIONS_EX']['item']['COND_VALUE']
            resErrorMsg = cpiResponse['ns0:SD_SALESDOCUMENT_CREATEResponse']['RETURN']['item']
            self.responseUpdateAtCart(resMatCost,resErrorMsg)
            self.delete_quote_msgs()
        except Exception as e:
            Log.Info('Error:'+str(e))
            resMatCost = ''
            resErrorMsg = cpiResponse['ns0:SD_SALESDOCUMENT_CREATEResponse']['RETURN']['item']
            self.responseUpdateAtCart(resMatCost,resErrorMsg)
           

# Usage
partNumber = context.Product.PartNumber
vcpPro = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(partNumber,'True','False'))
proIsComplete = context.Product.IsComplete

if vcpPro and proIsComplete:
    processor = CostAPI(context)
    processor.process()
