import time

def fieldsValidation(row):
    # disChanl = row["DC"]
    # salesOrg = row["SORG"]
    # dision = row["DIV"]
    # plant = row["Plant"]

    fields = {
        "Distribution Channel": row["DC"],
        "Sales Org": row["SORG"],
        "Division": row["DIV"],
        "Plant": row["Plant"]
    }

    missing = [label for label, value in fields.items() if not value]

    if not missing:
        return True
    elif len(missing) == 1:
        return  missing[0] + " is missing for Material number:"+str(row["MATERIAL"])+" and Plant:"+str(row["Plant"])
    elif len(missing) == 2:
        return missing[0] + " and " + missing[1] + " are missing for Material number:"+str(row["MATERIAL"])+" and Plant:"+str(row["Plant"])
    else:
        return ", ".join(missing[:-1]) + " and " + missing[-1] + " are missing for Material number:"+str(row["MATERIAL"])+" and Plant:"+str(row["Plant"])



def update_MaterialTable(data):
    #checking if existing record is there with matching material number and plant
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    for row in data:
        msg = fieldsValidation(row)
        if msg != True:
            Log.Info(msg)
            continue
        Log.Info(str(row))
        plant = row["Plant"]
        material = row["MATERIAL"]
        
        # plant = row["Plant"]
        #checking if the product is there or not
        q = "Select PRODUCT_CATALOG_CODE from PRODUCTS where PRODUCT_CATALOG_CODE = '{0}'".format(material)
        res = SqlHelper.GetList(q)
        if len(res) != 0:
            user_info = SqlHelper.GetFirst("select ID from users where username = 'COM_USER_S4CPQINT'")
            query = "select MATERIAL, Plant, PROFITCENTER, CpqTableEntryId from LBF_QU_MAT_COST where MATERIAL = '{0}' and Plant = '{1}'".format(material, plant)
            res = SqlHelper.GetList(query)
            if len(res) == 0:
                tableInfo = SqlHelper.GetTable("LBF_QU_MAT_COST")
                tablerow = {
                    		"Plant" : plant,
                            "MATERIAL" : material,
                            "GROSS_WEIGHT":float(row["GROSS_WEIGHT"]),
                            "NET_WEIGHT": float(row["NET_WEIGHT"]),
                            "SAP_COST": row["SAP_COST"],
                            "WEIGHT_UNIT": row["WEIGHT_UNIT"],
                            "PRICE_UNIT": row["PRICE_UNIT"],
                            "SORG":row["SORG"],
                            "DC":row["DC"],
                           	"DIV": row["DIV"],
                            "PROFITCENTER":row["PROFITCENTER"],
                    		"CpqTableEntryDateModified" : current_time,
                    		"CpqTableEntryModifiedBy" : user_info.ID
                           }
                tableInfo.AddRow(tablerow)
                upsertResult = SqlHelper.Upsert(tableInfo)
                Log.Info("Add " + str(upsertResult))
            else:
                for rec in res:
                    CpqTableEntryId = rec.CpqTableEntryId
                    tableInfo = SqlHelper.GetTable("LBF_QU_MAT_COST")
                    tablerow = { 
                        		"Plant" : plant,
                                "CpqTableEntryId":CpqTableEntryId,
                                "MATERIAL" : material,
                                "GROSS_WEIGHT":float(row["GROSS_WEIGHT"]),
                                "NET_WEIGHT": float(row["NET_WEIGHT"]),
                                "SAP_COST": row["SAP_COST"],
                                "WEIGHT_UNIT": row["WEIGHT_UNIT"],
                                "PRICE_UNIT": row["PRICE_UNIT"],
                                "SORG":row["SORG"],
                                "DC":row["DC"],
                                "DIV": row["DIV"],
                                "PROFITCENTER":row["PROFITCENTER"],
                                "CpqTableEntryDateModified": current_time,
                                "CpqTableEntryModifiedBy" : user_info.ID
                               }
                    tableInfo.AddRow(tablerow)
                    SqlHelper.Upsert(tableInfo)
                    Log.Info("Update")
        else:
			Log.Info("Product is not there in CPQ")
Log.Info("LBF_GS_MultiSalesResponse request---->"+str(Param))
Log.Info("LBF_GS_MultiSalesResponse request Param---->"+str(JsonHelper.Serialize(Param)))
#Log.Info("LBF_GS_MultiSalesResponse request Param.data---->"+str(JsonHelper.Serialize(Param.data)))

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