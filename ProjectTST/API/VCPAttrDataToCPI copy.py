class CostAPICall():
    def __init__(self):
        self.totAttr = Product.Attributes
        self.editableAttr = [attr.Name for attr in self.totAttr if str(attr.Access) == 'Editable']
        # self.DC = ''
        # self.SalesOrg = '1000'

    def run(self):
        cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/Replicate_Cost_to_S4' # awaiting from CPI team
        requestData = {
            'ORDER_HEADER_IN' :{
                'DOC_TYPE' : 'ZOR',
                'SALES_ORG' : '1000',
                'DISTR_CHAN' : '10',
                'DIVISION' : '10',
                'PURCH_NO':'01390029'
            },
            'ORDER_ITEMS_IN' :{
                'ITM_NUMBER':'000001',
                'PO_ITM_NO':'1',
                'MATERIAL':'HH_NEW_T_RAIL',
                'TARGET_QTY':'1', 
            },

            'ORDER_PARTNERS':{
                'SP' : {
                    'PARTN_ROLE':'SP',
                    'PARTN_NUMB':'123456',
                },
                'SH' : {
                    'PARTN_ROLE':'SH',
                    'PARTN_NUMB':'87654321',
                }
            },
            
            'ORDER_SCHEDULE_IN':{
                'ITM_NUMBER' : '000001',
                'SCHED_LINE' : '0001',
                'REQ_QTY' : '1'
            },

            'ORDER_CFGS_REF' : {
                'POSEX':'000001',
                'CONFIG_ID':'000001',
                'ROOT_ID':'00000001',
                'SCE':'1',
                'COMPLETE':'T',
                'CONSISTENT':'T',
            },

            'ORDER_CFGS_INST':{
                'CONFIG_ID':'000001',
                'INST_ID':'00000001',
                'OBJ_TYPE' : 'MARA',
                'CLASS_TYPE':'300',
                'OBJ_KEY ':'HH_NEW_T_RAIL',
                'QUANTITY':'1',
            },

            'ORDER_CFGS_VALUE':[
                {
                    'CONFIG_ID' : '000001',
                    'INST_ID':'00000001',
                    'CHARC':'Rail Section',
                    'VALUE':'100-8'
                },
                {
                    'CONFIG_ID' : '000001',
                    'INST_ID':'00000001',
                    'CHARC':'Rail Grade',
                    'VALUE':'Head Hardened '
                },
                {
                    'CONFIG_ID' : '000001',
                    'INST_ID':'00000001',
                    'CHARC':'Overall Lg- Feet',
                    'VALUE':'1'
                }
            ]
        
        }
        cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, requestData)
        Trace.Write(str(cpiResponse))

object = CostAPICall().run()