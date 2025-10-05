class GetUOM():
    def __init__(self,params):
        self.params = params

    def GetUOM_Mapping_Data(self):
        data = SqlHelper.GetList("select S4CPI,CPQDisplayUOM from LBF_QU_UOM_MAPPING_FIELDS")
        json_data = {}
        for record in data:
            json_data[record.S4CPI] = record.CPQDisplayUOM
        return json_data

    def run(self):
        if self.params.Action == "UOMMapping":
            return self.GetUOM_Mapping_Data()

response_data = GetUOM(Param).run()
ApiResponse = ApiResponseFactory.JsonResponse(response_data)