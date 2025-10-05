import time

class SalesTextUpdate():
    def __init__(self):
        self.current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    def MatUpdate(self, data):
        #checking if existing record is there with matching material number and plant
        for row in data:
            Log.Info(str(row))
            material = row["Material"]
            salesOrg = row["SalesOrg"]
            DC = row["DC"]
            #checking if the product is there or not
            q = "Select PRODUCT_CATALOG_CODE from PRODUCTS where PRODUCT_CATALOG_CODE = '{0}'".format(material)
            res = SqlHelper.GetList(q)
            if len(res) != 0:
                user_info = SqlHelper.GetFirst("select ID from users where username = 'COM_USER_S4CPQINT'")
                query = "select Material, SalesOrg,DC,CpqTableEntryId from LBF_QU_SALESORG_INFO where Material = '{0}' and SalesOrg = '{1}' and DC = '{2}'".format(material, salesOrg,DC)
                res = SqlHelper.GetList(query)
                if len(res) == 0:
                    tableInfo = SqlHelper.GetTable("LBF_QU_SALESORG_INFO")
                    tablerow = {
                                "Material" : material,
                                "Description" : str(row["Description"]),
                                "SalesOrg":salesOrg,
                                "DC": DC,
                                "SalesText": str(row["SalesText"]),
                                "CpqTableEntryDateModified" : self.current_time,
                                "CpqTableEntryModifiedBy" : user_info.ID
                            }
                    tableInfo.AddRow(tablerow)
                    upsertResult = SqlHelper.Upsert(tableInfo)
                    Log.Info("SalesOrgInfo table record added " + str(upsertResult))
                else:
                    for rec in res:
                        CpqTableEntryId = rec.CpqTableEntryId
                        tableInfo = SqlHelper.GetTable("LBF_QU_SALESORG_INFO")
                        tablerow = { 
                                    "Material" : material,
                                    "Description" : str(row["Description"]),
                                    "SalesOrg":salesOrg,
                                    "DC": DC,
                                    "SalesText": str(row["SalesText"]),
                                    "CpqTableEntryId":CpqTableEntryId,
                                    "CpqTableEntryDateModified" : self.current_time,
                                    "CpqTableEntryModifiedBy" : user_info.ID
                                    }
                        tableInfo.AddRow(tablerow)
                        SqlHelper.Upsert(tableInfo)
                        Log.Info("SalesOrgInfo table Updated")
            else:
                Log.Info("Product is not there in CPQ")



#Log.Info("LBF_GS_SalesTextUpdate  request---->"+str(Param))
#Log.Info("LBF_GS_SalesTextUpdate  request Param---->"+str(JsonHelper.Serialize(Param)))
#Log.Info("LBF_GS_SalesTextUpdate  request Param.data---->"+str(JsonHelper.Serialize(Param.data)))

Log.Info("LBF_GS_SalesTextUpdate Param---->"+str(Param))
Log.Info("LBF_GS_SalesTextUpdate Param.data---->"+str(Param.data))
data = JsonHelper.Serialize(Param.data)
des_data = JsonHelper.Deserialize(data)

if (Param is not None and des_data is not None):
    # data = JsonHelper.Serialize(Param.data)
    # des_data = JsonHelper.Deserialize(data)
    Log.Info("LBF_GS_SalesTextUpdate des_data---->"+str(des_data))
    res = SalesTextUpdate().MatUpdate(des_data)

    ApiResponse = ApiResponseFactory.JsonResponse(res)
else:
    #Log.Info('Executing...')
    ApiResponse = ApiResponseFactory.JsonResponse("Failed")