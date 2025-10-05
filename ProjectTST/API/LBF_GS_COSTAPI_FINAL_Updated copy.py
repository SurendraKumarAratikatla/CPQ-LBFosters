class CostAPI:
    def __init__(self, context):
        self.context = context
        self.Product = context.Product
        self.currentItemId = 0
        self.plant = ''
        self.errMsg = ''
        self.payload = {
            'ORDER_HEADER_IN': {
                'DOC_TYPE': 'ZSIM',
                'SALES_ORG': '1000',
                'DISTR_CHAN': '10',
                'DIVISION': '20',
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

    def accessMatCostTbl(self):
        prtNo = self.Product.PartNumber
        data = SqlHelper.GetFirst("SELECT * from LBF_QU_MAT_COST WHERE MATERIAL = '{0}' ".format(prtNo))
        if data:
            self.plant = data.Plant
        else:
            self.plant = ''

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
                Log.Info(item['TYPE'])
                if str(item['TYPE']) == "E":
                    self.errMsg += str(item['MESSAGE']) + '. '
                    Log.Info(item['MESSAGE'])
            pass

        elif str(type(resErrorMsg)) == "<type 'list'>":
            if str(resErrorMsg['TYPE']) == "E":
                self.errMsg += str(item['MESSAGE']) + '. '

    def update_header(self):
        """Update header information based on the quote."""
        self.payload['ORDER_HEADER_IN']['PURCH_NO'] = self.context.Quote.QuoteNumber
        self.payload['ORDER_ITEMS_IN']['MATERIAL'] = self.Product.PartNumber
        self.payload['ORDER_ITEMS_IN']['PLANT'] = self.plant
        self.payload['ORDER_ITEMS_IN']['PO_ITM_NO'] = str(self.currentItemId)
        self.payload['ORDER_CFGS_INST']['OBJ_KEY'] = self.Product.PartNumber
        #Log.Info('self.currentItemId-- AT-->'+str(self.currentItemId))
        self.payload['ORDER_CFGS_REF']['POSEX'] = "00000"+str(self.currentItemId)

    def update_partners(self):
        """Update partner information in the payload."""
        involved_parties = self.context.Quote.GetInvolvedParties()
        for party in involved_parties:
            self.payload['ORDER_PARTNERS'][party.PartnerFunctionKey] = {
                'PARTN_ROLE': party.PartnerFunctionKey,
                'PARTN_NUMB': party.ExternalId
            }

    def populate_cfgs_value(self):
        """Populate ORDER_CFGS_VALUE with editable attributes."""
        tot_attr = self.Product.Attributes
        editable_attr = [attr.Name for attr in tot_attr if str(attr.Access) == 'Editable']

        for item in editable_attr:
            try:
                #value = self.Product.Attr(item).GetValue()
                valueTemp = self.Product.Attr(item).SelectedValue.ValueCode
                value = self.Product.Attr(item).GetValue() if valueTemp == "DefaultValue" else valueTemp
                systemId = self.Product.Attr(item).SystemId
            except Exception as e:
                value = None

            self.payload['ORDER_CFGS_VALUE'].append({
                'CONFIG_ID': '000001',
                'INST_ID': '00000001',
                'CHARC': systemId,
                'VALUE': value
            })


    def responseUpdateAtCart(self,resMatCost,resErrorMsg):
        # Error msg
        Log.Info('resErrorMsg---'+str(resErrorMsg))
        Log.Info("TYPE: resErrorMsg----"+str(type(resErrorMsg)))
        self.getCostErrorMsgs(resErrorMsg)
        Log.Info("self.errMsg----"+str(self.errMsg))
        Log.Info('COST API Response COST if-->'+str(resMatCost))
        for item in context.Quote.GetAllItems():
            if str(int(item.RolledUpQuoteItem)) == str(int(self.currentItemId)):
                Log.Info('COST API Response COST elif-->'+str(resMatCost))
                if self.errMsg:
                    item['LBF_QU_COSTSTATUS'] = "Error"
                    item['LBF_QU_COSTERROR'] = str(self.errMsg)
                    break
                else:
                    item['LBF_QU_MAT_CST'] = str(resMatCost)
                    item['LBF_QU_COSTSTATUS'] = "Success"
                    item['LBF_QU_COSTERROR'] = 'Cost added to the line item.'
                    break

    def process(self):
        """Main process to update the payload."""
        self.getRolledupItemId()
        self.accessMatCostTbl()
        self.update_header()
        self.update_partners()
        self.populate_cfgs_value()
        Log.Info("Final Payload:")
        Log.Info(str(self.payload))
        data = JsonHelper.Serialize(self.payload)
        Log.Info(str(data))
        cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/Replicate_Cost_to_S4'
        try:    
            cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, data)
            Log.Info(str(cpiResponse))
            resMatCost = cpiResponse['ns0:SD_SALESDOCUMENT_CREATEResponse']['CONDITIONS_EX']['item']['COND_VALUE']
            resErrorMsg = cpiResponse['ns0:SD_SALESDOCUMENT_CREATEResponse']['RETURN']['item']
            self.responseUpdateAtCart(resMatCost,resErrorMsg)
        except Exception as e:
            Log.Info('Error:'+str(e))
            resMatCost = ''
            resErrorMsg = cpiResponse['ns0:SD_SALESDOCUMENT_CREATEResponse']['RETURN']['item']
            self.responseUpdateAtCart(resMatCost,resErrorMsg)
           

# Usage
processor = CostAPI(context)
processor.process()
