from LBF_GS_CREATEBEARERTOKEN import creating_bearer_token

class CopyLineItems:
    def __init__(self, ref_quote_number):
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

    def get_ref_quote_items(self):
        ref_quote_id = QuoteHelper.Get(str(self.ref_quote_number)).Id
        self.url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{0}/items'.format(ref_quote_id)
        encodedKeys = "Bearer " + str(self.bearer_token)
        self.headers = {"Authorization": encodedKeys}
        quoteHeaderObj = RestClient.Get(self.url, self.headers)
        serializedQuote_data = JsonHelper.Serialize(quoteHeaderObj)
        #refQuoteJSON = JsonHelper.Deserialize(serializedQuote_data)
        return serializedQuote_data
    
    def copy_items_to_currentquote(self, refQuoteJSON):
        curr_quote_id = context.Quote.Id
        url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{0}/items'.format(curr_quote_id)
        #encodedKeys = "Bearer " + str(self.bearer_token)
        #self.headers = {"Authorization": encodedKeys}
        Trace.Write(str(self.headers))
        Trace.Write(str(refQuoteJSON))
        Trace.Write(str(url))
        response = RestClient.Post(url, str(refQuoteJSON), self.headers)
        Trace.Write(str(JsonHelper.Deserialize(JsonHelper.Serialize(response))))

    def run(self):
        print('quote number is...'+str(self.ref_quote_number))
        auth = self.GetBearerToken()
        if auth != "error":
            self.bearer_token = auth
            refQuoteJSON = self.get_ref_quote_items()
            Trace.Write(refQuoteJSON)
            if "The request is invalid." not in refQuoteJSON:
                self.copy_items_to_currentquote(refQuoteJSON)
            else:
                Log.Info("Something went wrong in get items call! please check")
        elif auth == "error":
            Log.Info("Authentication failed!")


ref_quote_number = context.Quote.GetCustomField('LBF_CF_QuoteNumbertoCopyLines').Value #01390218
if ref_quote_number:
    object = CopyLineItems(ref_quote_number).run()
