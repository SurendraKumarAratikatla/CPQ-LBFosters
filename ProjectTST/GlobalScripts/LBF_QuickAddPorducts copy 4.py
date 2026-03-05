class quickadd():
    def __init__(self, params):
        self.params = params

    def run(self):
        Log.Info("LBF_QuickAddPorducts mainmodel ---"+str(type(self.params.mainmodel)))
        mainmodel = JsonHelper.Deserialize(JsonHelper.Serialize(self.params.mainmodel))
        Log.Info("mainmodel ---"+str(mainmodel))
        if mainmodel:
        quickaddpro = SqlHelper.GetList("select TOP 5 * from PRODUCTS WHERE PRODUCT_NAME LIKE '{}'".format(str(self.params.searchval)+"%"))
        listofquickaddpro = []
        i = 0
        for item in quickaddpro:
            tempdict = {}
            tempdict['id'] = item.PRODUCT_ID
            tempdict['name'] = item.PRODUCT_NAME
            tempdict['partNumber'] = item.PRODUCT_CATALOG_CODE
            tempdict['description'] = item.PRODUCT_DESCRIPTION
            listofquickaddpro.append(tempdict)

        for item in mainmodel:
            # Log.Info("LBF_QuickAddPorducts.partNumber ---"+str(item.partNumber))
            item['partNumber']= listofquickaddpro[i]['partNumber']
            item['name'] = listofquickaddpro[i]['name']
            item['id'] = listofquickaddpro[i]['id']
            item['description'] = listofquickaddpro[i]['description']
            i += 1

        serData = JsonHelper.Serialize(mainmodel)
        data = JsonHelper.Deserialize(serData)

        #Log.Info("LBF_QuickAddPorducts data-------->"+str(data))
        return data


object = quickadd(Param).run()

ApiResponse = ApiResponseFactory.JsonResponse(object)