class quickadd():
    def __init__(self, params):
        self.params = params

    def run(self):
        Log.Info("LBF_QuickAddPorducts mainmodel ---"+str(self.params.mainmodel))
        mainmodel = self.params.mainmodel
        listofquickaddpro = []
        if mainmodel:
            quickaddpro = SqlHelper.GetList("select TOP 5 * from PRODUCTS WHERE PRODUCT_NAME LIKE '{}'".format(str(self.params.searchval)+"%"))
            if quickaddpro:
                Log.Info("LBF_QuickAddPorducts quickaddpro-------->"+str(quickaddpro))
                for item in quickaddpro:
                    tempdict = {}
                    tempdict['id'] = item.PRODUCT_ID
                    tempdict['name'] = item.PRODUCT_NAME
                    tempdict['partNumber'] = item.PRODUCT_CATALOG_CODE
                    tempdict['description'] = item.PRODUCT_DESCRIPTION
                    listofquickaddpro.append(tempdict)

        serData = JsonHelper.Serialize(listofquickaddpro)
        data = JsonHelper.Deserialize(serData)

        Log.Info("LBF_QuickAddPorducts data-------->"+str(data))
        return data

object = quickadd(Param).run()

ApiResponse = ApiResponseFactory.JsonResponse(object)