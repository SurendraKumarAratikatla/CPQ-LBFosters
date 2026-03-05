class quickadd():
    def __init__(self, params):
        self.params = params

    def run(self):
        Log.Info("LBF_QuickAddPorducts mainmodel ---"+str(type(self.params.mainmodel)))
        mainmodel = JsonHelper.Deserialize(JsonHelper.Serialize(self.params.mainmodel))
        Log.Info("mainmodel ---"+str(mainmodel))
        quickaddpro = SqlHelper.GetList("select TOP 5 * from PRODUCTS WHERE PRODUCT_NAME LIKE '{}'".format(str(self.params.searchval)+"%"))
        for item in mainmodel:
            Log.Info("LBF_QuickAddPorducts.partNumber ---"+str(item['partNumber']))

        serData = JsonHelper.Serialize(quickaddpro).replace("PRODUCT_ID","id").replace("PRODUCT_NAME","name").replace("PRODUCT_CATALOG_CODE","partNumber").replace("PRODUCT_DESCRIPTION","description")
        data = JsonHelper.Deserialize(serData)

        #Log.Info("LBF_QuickAddPorducts data-------->"+str(data))
        return data


object = quickadd(Param).run()

ApiResponse = ApiResponseFactory.JsonResponse(object)