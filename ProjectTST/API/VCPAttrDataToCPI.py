class CostAPICall():
    def __init__(self):
        self.totAttr = Product.Attributes
        self.editableAttr = [attr.Name for attr in self.totAttr if str(attr.Access) == 'Editable']
        self.DC = ''
        self.SalesOrg = '1000'

    def run(self):
        cpiEndUrl = '' # awaiting from CPI team
        requestData = {}
        cpiResponse = AuthorizedRestClient.Post('Integration', cpiEndUrl, str(requestData))

object = CostAPICall().run()