class unHideProducts():
    def __init__(self, params):
        self.totalSellingPrice = 0.0
        self.params = params

    def unHideCheck(self, productData):
        Log.Info("productData----"+str(productData))
        sqlData = SqlHelper.GetFirst("select * from LBF_QU_PRODUCT_RESPONDER where ProductName = '{0}'".format(productData))
        if sqlData:
            return 'Exists'
        else:
            return 'Not Exists'
        
    def run(self):
        if self.params.Action == "responderUnhide":
            self.unHideCheck(self.params.Data)

Log.Info("Param....."+str(Param))
response_data = unHideProducts(Param).run()
ApiResponse = ApiResponseFactory.JsonResponse(response_data)
