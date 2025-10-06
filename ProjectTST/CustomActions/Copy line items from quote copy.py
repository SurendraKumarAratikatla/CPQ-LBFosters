from LBF_GS_CREATEBEARERTOKEN import creating_bearer_token
from Scripting.Quote import MessageLevel

class CopyLineItems:
    def __init__(self, ref_quote_number):
        self.quoteInfo = QuoteHelper.Get(context.Quote.QuoteNumber)
        self.ref_quote_number = ref_quote_number
        self.bearer_token = ''
        self.headers = ''
        self.url = ''

    def GetBearerToken(self):
        response = creating_bearer_token()
        if response[1] == 'success':
            stream = RestClient.DeserializeJson(StreamReader(response[0].GetResponseStream()).ReadToEnd())
            return stream.access_token
        else:
            return 'error'
        
    def quoteMsg(self,msgType, curMsg):
        if msgType == "Success":
            self.quoteInfo.AddMessage(str(curMsg), MessageLevel.Success, False)
        elif msgType == "Warning":
            self.quoteInfo.AddMessage(str(curMsg), MessageLevel.Warning, False)
        elif msgType == "Error":
            self.quoteInfo.AddMessage(str(curMsg), MessageLevel.Error, False)
        #added this line for reseting reference customfield once items has copied
        context.Quote.GetCustomField('LBF_CF_QuoteNumbertoCopyLines').Value = ""

    def deleteQuoteMsgs(self):
        for msg in self.quoteInfo.Messages:
            if str(msg.Content) == "Items added successfully!" or str(msg.Content) == "Items not found for the provided reference quote number." or str(msg.Content) == "Invalid reference quote number, please check."  or str(msg.Content) == "Please provide reference quote number.":
                self.quoteInfo.DeleteMessage(msg.Id)

    def get_ref_quote_items(self):
        ref_quote_id = QuoteHelper.Get(str(self.ref_quote_number)).Id
        self.url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{0}/items'.format(ref_quote_id)
        encodedKeys = "Bearer " + str(self.bearer_token)
        self.headers = {"Authorization": encodedKeys}
        quoteHeaderObj = RestClient.Get(self.url, self.headers)
        serializedQuote_data = JsonHelper.Serialize(quoteHeaderObj)
        return serializedQuote_data

    def copy_items_to_currentquote(self, refQuoteJSON):
        curr_quote_id = context.Quote.Id
        url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{0}/items'.format(curr_quote_id)
        response = RestClient.Post(url, str(refQuoteJSON), self.headers)
        if response:
            self.quoteMsg('Success','Items added successfully!')

    def run(self):
        # delete previous quote messages
        self.deleteQuoteMsgs()
        if self.ref_quote_number:
            # reference quote number check
            quoteNumber = SqlHelper.GetFirst("select QuoteNumber from sys_Quote where QuoteNumber='{}'".format(str(self.ref_quote_number)))
            if quoteNumber:
                auth = self.GetBearerToken()
                if auth != "error":
                    self.bearer_token = auth
                    refQuoteJSON = self.get_ref_quote_items()
                    if list(refQuoteJSON) != []:
                        if "The request is invalid." not in refQuoteJSON:
                            self.copy_items_to_currentquote(refQuoteJSON)
                        else:
                            Log.Info("Something went wrong in get items call, please check.")
                    else:
                        self.quoteMsg('Warning','Items not found for the provided reference quote number.')
                elif auth == "error":
                    Log.Info("Authentication failed!")
            else:
                self.quoteMsg('Error','Invalid reference quote number, please check.')
        else:
            self.quoteMsg('Error','Please provide reference quote number.')

ref_quote_number = (context.Quote.GetCustomField('LBF_CF_QuoteNumbertoCopyLines').Value) #01390218
if ref_quote_number:
    object = CopyLineItems(ref_quote_number).run()
