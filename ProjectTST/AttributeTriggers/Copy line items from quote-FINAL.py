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
    
    def deleteQuoteMsgs(self):
        for msg in self.quoteInfo.Messages:
            if str(msg.Content) == "Items added successfully!" or str(msg.Content) == "Items not found for the provided reference quote number." or str(msg.Content) == "Invalid reference quote number, please check." or str(msg.Content) =="Quote number missing, enter quote number to copy lines." or str(msg.Content) =="Error while adding the line items, please check the logs for more info.":
                self.quoteInfo.DeleteMessage(msg.Id)

    def get_ref_quote_items(self):
        ref_quote_id = QuoteHelper.Get(str(self.ref_quote_number)).Id
        self.url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{0}/items'.format(ref_quote_id)
        encodedKeys = "Bearer " + str(self.bearer_token)
        self.headers = {"Authorization": encodedKeys}
        Trace.Write('11111111111111111'+str(self.bearer_token))
        quoteHeaderObj = RestClient.Get(self.url, self.headers)
        Trace.Write('22222222222222222'+str(quoteHeaderObj))
        #serializedQuote_data = JsonHelper.Serialize(quoteHeaderObj)
        serializedQuote_data = JsonHelper.Serialize(quoteHeaderObj) if quoteHeaderObj else quoteHeaderObj
        Trace.Write(serializedQuote_data)
        Trace.Write(str(type(serializedQuote_data)))
        Trace.Write("3333333333333333")
        formated_json = (serializedQuote_data).replace('”', '"').replace('“', '"').replace('’', "'").replace('‘', "'").replace("–","-").replace("—","-")
        Trace.Write(formated_json)
        Trace.Write("4444444444444444")
        return (formated_json)
    
    def copy_items_to_currentquote(self, refQuoteJSON):
        curr_quote_id = context.Quote.Id
        url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{0}/items'.format(curr_quote_id)
        try:
            Trace.Write("try..")
            response = RestClient.Post(url, JsonHelper.Serialize(refQuoteJSON), self.headers)
        except:
            Trace.Write("except..")
            response = RestClient.Post(url, (refQuoteJSON), self.headers)
            Trace.Write("except..")

        if response:
            self.quoteMsg('Success','Items added successfully!')

    def run(self):
        print('quote number is...'+str(self.ref_quote_number))
        # delete previous quote messages
        self.deleteQuoteMsgs()
        if self.ref_quote_number:
            # reference quote number check
            quoteNumber = SqlHelper.GetFirst("select QuoteNumber from sys_Quote where QuoteNumber='{}'".format(str(self.ref_quote_number)))
            if quoteNumber:
                auth = self.GetBearerToken()
                if auth != "error":
                    self.bearer_token = auth
                    Trace.Write("refQuoteJSON==========: ")
                    refQuoteJSON = self.get_ref_quote_items()
                    Trace.Write("refQuoteJSON: "+str(refQuoteJSON))
                    if list(refQuoteJSON) != []:
                        # if "The request is invalid." not in refQuoteJSON and 'error' not in refQuoteJSON:
                        if "ParentRolledUpItemNumber" in refQuoteJSON:
                            self.copy_items_to_currentquote(refQuoteJSON)
                        else:
                            Log.Info("ERROR:Copy line items from quote: "+str(refQuoteJSON))
                            self.quoteMsg('Error','Error while adding the line items, please check the logs for more info.')
                    else:
                        self.quoteMsg('Warning','Items not found for the provided reference quote number.')
                elif auth == "error":
                    Log.Info("Authentication failed!")
            else:
                self.quoteMsg('Error','Invalid reference quote number, please check.')
        else:
            self.quoteMsg('Error','Quote number missing, enter quote number to copy lines.')

ref_quote_number = (context.Quote.GetCustomField('LBF_CF_QuoteNumbertoCopyLines').Value).strip() #01390218
object = CopyLineItems(ref_quote_number).run()
