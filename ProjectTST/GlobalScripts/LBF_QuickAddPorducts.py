class quickadd():
    def __init__(self, params):
        self.params = params

    def run(self):
        #Log.Info("LBF_QuickAddPorducts ---"+str(self.params))
        quickaddpro = SqlHelper.GetList("select TOP 5 PRODUCT_NAME, PRODUCT_CATALOG_CODE from PRODUCTS WHERE PRODUCT_NAME LIKE '{}'".format(str(self.params.searchval)+"%"))
        #serData = JsonHelper.Serialize(quickaddpro).replace("PRODUCT_ID","id").replace("PRODUCT_NAME","name").replace("PRODUCT_CATALOG_CODE","partNumber").replace("PRODUCT_DESCRIPTION","description")
        #data = JsonHelper.Deserialize(serData)
        # add missing fields
        data = []
        for item in quickaddpro:
            data.append(item.PRODUCT_CATALOG_CODE)
        #Log.Info("LBF_QuickAddPorducts data-------->"+str(data))
        return data


object = quickadd(Param).run()

ApiResponse = ApiResponseFactory.JsonResponse(object)



