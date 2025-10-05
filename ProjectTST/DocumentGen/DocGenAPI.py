requestData = QuoteHelper.Get('01470076').GetLatestGeneratedDocumentInBytes()
cpiEndUrl = 'https://lb-foster-integration-suite-nonprod-br62rx5d.it-cpi019-rt.cfapps.us10-002.hana.ondemand.com/http/TestDoc' # awaiting from CPI team
cpiResponse = AuthorizedRestClient.Post('CPQ', cpiEndUrl, str(requestData))


from Scripting import IConvert
from Scripting.IConvert import ToBase64String

requestData = QuoteHelper.Get('01470076').GetLatestGeneratedDocumentInBytes()
bytes = { 2, 4, 6, 8, 10, 12, 14, 16, 18, 20 }

base64 = Convert.ToBase64String(requestData)