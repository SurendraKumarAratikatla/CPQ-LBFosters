
def update_MaterialTable(data):
    #checking if existing record is there with matching material number and plant
    
    for row in data:
        Log.Info(str(row))
        plant = row["Plant"]
        material = row["MATERIAL"]
        query = "select MATERIAL, Plant, CpqTableEntryId from LBF_QU_MAT_COST where MATERIAL = '{0}' and Plant = '{1}'".format(material, plant)
        res = SqlHelper.GetList(query)
        if len(res) == 0:
            tableInfo = SqlHelper.GetTable("LBF_QU_MAT_COST")
            tablerow = { 
                "Plant" : plant,
                        "MATERIAL" : material,
                        "GROSS_WEIGHT":row["GROSS_WEIGHT"],
                        "NET_WEIGHT": row["NET_WEIGHT"],
                        "SAP_COST": row["SAP_COST"],
                        "WEIGHT_UNIT": row["WEIGHT_UNIT"],
                        "PRICE_UNIT": row["PRICE_UNIT"],
                        "SORG":row["SORG"],
                        "DC":row["DC"],
                       "DIV": row["DIV"],
                       "MAVP": row["MAVP"],
                       "STD": row["STD"]
                       }
            tableInfo.AddRow(tablerow)
            upsertResult = SqlHelper.Upsert(tableInfo)
            Log.Info("Add " + str(upsertResult))
        else:
            for rec in res:
                CpqTableEntryId = rec.CpqTableEntryId
                tableInfo = SqlHelper.GetTable("LBF_QU_MAT_COST")
                tablerow = { "Plant" : plant,
                            "CpqTableEntryId":CpqTableEntryId,
                            "MATERIAL" : material,
                            "GROSS_WEIGHT":row["GROSS_WEIGHT"],
                            "NET_WEIGHT": row["NET_WEIGHT"],
                            "SAP_COST": row["SAP_COST"],
                            "WEIGHT_UNIT": row["WEIGHT_UNIT"],
                            "PRICE_UNIT": row["PRICE_UNIT"],
                            "SORG":row["SORG"],
                            "DC":row["DC"],
                           "DIV": row["DIV"],
                           "MAVP": row["MAVP"],
                           "STD": row["STD"]
                           }
                tableInfo.AddRow(tablerow)
                SqlHelper.Upsert(tableInfo)
                Log.Info("Update ")




Log.Info("LBF_GS_MultiSalesResponse request data---->"+str(JsonHelper.Serialize(Param)))
if (Param is not None and Param.data is not None):
    data = JsonHelper.Serialize(Param.data)
    Log.Info("LBF_GS_MultiSalesResponse Param.data---->"+str(JsonHelper.Serialize(Param.data)))
    res = update_MaterialTable(Param.data)
    
    #url = RequestContext.Url
    #Log.Info(str(url))
    ApiResponse = ApiResponseFactory.JsonResponse(res)
else:
    Log.Info('Running')
    ApiResponse = ApiResponseFactory.JsonResponse("Failed")