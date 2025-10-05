from Scripting.Quote import MessageLevel
class CustomerInfoCheck:
    def __init__(self):
        self.quoteInfo = QuoteHelper.Get(context.Quote.QuoteNumber)
        
    def deleteQuoteMsgs(self,curMsg):
        Log.Info("4444444444444444")
        for msg in self.quoteInfo.Messages:
            Log.Info("55555555555555555")
            if curMsg == "":
                Log.Info("77777777777777777")
                self.quoteInfo.DeleteMessage(msg.Id)
                break
            elif str(msg.Content) != str(curMsg):
                Log.Info("66666666666666666666")
                self.quoteInfo.DeleteMessage(msg.Id)
                self.quoteInfo.AddMessage(str(curMsg), MessageLevel.Error, False)
                break
            

    def inv_party_check(self):
        involved_parties = self.quoteInfo.GetInvolvedParties()
        ship_to = sold_to = None
        sh = sp = False
        for party in involved_parties:
            if party.PartnerFunctionName == "Ship-to party":
                ship_to = party.ExternalId
                sh = True
            elif party.PartnerFunctionName == "Sold-to party":
                sold_to = party.ExternalId
                sp = True
        if not sp and not sh:
            curMsg = "Please enter Sold-to and Ship-to in Customer Info Tab"
            Log.Info("000000000000")
            self.deleteQuoteMsgs(curMsg)
        elif not sp:
            curMsg = "Please Enter Sold-to Party"
            Log.Info("11111111111111111")
            self.deleteQuoteMsgs(curMsg)
        elif not sh:
            curMsg = "Please Enter Ship-to Party"
            Log.Info("22222222222222222222222")
            self.deleteQuoteMsgs(curMsg)
        elif not ship_to.strip() or not sold_to.strip():
            curMsg = "Not a valid customer from S/4. Please enter a valid Sold-to and Ship-to from S/4"
            Log.Info("elif 3333333333333333333333")
            self.deleteQuoteMsgs(curMsg)
        else:
            Log.Info("else 3333333333333333333333")
            self.deleteQuoteMsgs("")

CustomerInfoCheck().inv_party_check()