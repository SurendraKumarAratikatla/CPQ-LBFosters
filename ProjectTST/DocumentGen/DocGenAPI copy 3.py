from Scripting import IConvert
from Scripting.IConvert import ToBase64String

class DocAPI():
    def __init__(self):
        self.quoteInfo = QuoteHelper.Get(context.Quote.QuoteNumber)

    def DocToCPI(self):
        quoteNumber = self.quoteInfo.QuoteNumber
        opportunityId = self.quoteInfo.OpportunityId
        cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/TestDoc'
        requestData = self.quoteInfo.GetLatestGeneratedDocumentInBytes()
        base64 = Convert.ToBase64String(requestData)
        try:
            cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, {'data':str(base64),'QuoteNumber':str(quoteNumber),'OpportunityId':str(opportunityId)})
        except:
            Log.Info("Error while sending the DOC. to CPI")

object = DocAPI().DocToCPI()








quoteNumber = '01470076'
quoteInfo = QuoteHelper.Get('01470076')
opportunityId = quoteInfo.OpportunityId
requestData = quoteInfo.GetLatestGeneratedDocumentInBytes()
base64 = Convert.ToBase64String(requestData)
cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/TestDoc'
cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, {'data':str(base64),'QuoteNumber':str(quoteNumber),'OpportunityId':str(opportunityId)})

