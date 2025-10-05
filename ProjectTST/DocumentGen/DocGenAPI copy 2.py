from Scripting import IConvert
from Scripting.IConvert import ToBase64String

quoteNumber = '01470076'
quoteInfo = QuoteHelper.Get('01470076')
opportunityId = quoteInfo.OpportunityId
requestData = quoteInfo.GetLatestGeneratedDocumentInBytes()
base64 = Convert.ToBase64String(requestData)
cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/TestDoc'
cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, {'data':str(base64),'QuoteNumber':str(quoteNumber),'OpportunityId':str(opportunityId)})

