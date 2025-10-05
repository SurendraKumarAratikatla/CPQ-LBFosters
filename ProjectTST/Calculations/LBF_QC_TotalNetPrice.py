

TotalNetPrice()


class Total():
    def __init__(self):
        self.totalSellingPrice = 0.0

    def TotalNetPrice(self):
        for item in context.Quote.GetAllItems():
            self.totalSellingPrice = self.totalSellingPrice + float(item['LBF_QU_SELPRICE'])
        context.Quote.Totals.Amount = float(self.totalSellingPrice)

        
    def run(self):
        self.TotalNetPrice()


object = Total().run()
