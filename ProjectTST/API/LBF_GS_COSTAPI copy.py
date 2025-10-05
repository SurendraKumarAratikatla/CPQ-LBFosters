class CostAPI:
    def __init__(self, context):
        self.context = context
        self.Product = context.Product
        self.plant = ''
        self.payload = {
            'ORDER_HEADER_IN': {
                'DOC_TYPE': 'ZOR',
                'SALES_ORG': '1000',
                'DISTR_CHAN': '10',
                'DIVISION': '10',
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
                'POSEX': '000001',
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

    def update_header(self):
        """Update header information based on the quote."""
        self.payload['ORDER_HEADER_IN']['PURCH_NO'] = self.context.Quote.QuoteNumber
        self.payload['ORDER_ITEMS_IN']['MATERIAL'] = self.Product.Name
        self.payload['ORDER_ITEMS_IN']['PLANT'] = self.plant
        self.payload['ORDER_CFGS_INST']['OBJ_KEY'] = self.Product.Name

    def update_partners(self):
        """Update partner information in the payload."""
        involved_parties = self.context.Quote.GetInvolvedParties()
        for party in involved_parties:
            self.payload['ORDER_PARTNERS'][party.PartnerFunctionKey] = {
                'PARTN_ROLE': party.PartnerFunctionKey,
                'PARTN_NUMB': party.PartnerNumber
            }

    def populate_cfgs_value(self):
        """Populate ORDER_CFGS_VALUE with editable attributes."""
        tot_attr = self.Product.Attributes
        editable_attr = [attr.Name for attr in tot_attr if str(attr.Access) == 'Editable']

        for item in editable_attr:
            try:
                #value = self.Product.Attr(item).GetValue()
                value = self.Product.Attr(item).SelectedValue.ValueCode
            except Exception as e:
                value = None

            self.payload['ORDER_CFGS_VALUE'].append({
                'CONFIG_ID': '000001',
                'INST_ID': '00000001',
                'CHARC': item,
                'VALUE': value
            })

    def process(self):
        """Main process to update the payload."""
        self.accessMatCostTbl()
        self.update_header()
        self.update_partners()
        self.populate_cfgs_value()
        Trace.Write("Final Payload:")
        Trace.Write(str(self.payload))
        data = JsonHelper.Serialize(self.payload)
        Log.Info(str(data))
        cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/Replicate_Cost_to_S4'
        cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, data)
        Log.Info(str(cpiResponse))




# Usage
processor = CostAPI(context)
processor.process()
