import time

class InforMatTblUpdate():
    def __init__(self):
        self.current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    def MatUpdate(self, data):
        #checking if existing record is there with matching material number and plant
        for row in data:
            Log.Info(str(row))
            partNumber = row["PARTNUMBER"]
            siteId = row["SITEID"]
            #checking if the product is there or not
            q = "Select PRODUCT_CATALOG_CODE from PRODUCTS where PRODUCT_CATALOG_CODE = '{0}'".format(partNumber)
            res = SqlHelper.GetList(q)
            if len(res) != 0:
                user_info = SqlHelper.GetFirst("select ID from users where username = 'COM_USER_S4CPQINT'")
                query = "select PARTNUMBER, SITEID,CpqTableEntryId from LBF_QU_INFOR_MAT_COST where PARTNUMBER = '{0}' and SITEID = '{1}'".format(partNumber, siteId)
                res = SqlHelper.GetList(query)
                if len(res) == 0:
                    tableInfo = SqlHelper.GetTable("LBF_QU_INFOR_MAT_COST")
                    tablerow = {
                                "PARTNUMBER" : partNumber,
                                "SITEID" : siteId,
                                "PART_SITE_ID":float(row["PART_SITE_ID"]),
                                "DESCRIPTION": float(row["DESCRIPTION"]),
                                "UNIT_COST_USD": row["UNIT_COST_USD"],
                                "UNIT_PRICE_USD": row["UNIT_PRICE_USD"],
                                "WEIGHT_G": row["WEIGHT_G"],
                                "CpqTableEntryDateModified" : self.current_time,
                                "CpqTableEntryModifiedBy" : user_info.ID
                            }
                    tableInfo.AddRow(tablerow)
                    upsertResult = SqlHelper.Upsert(tableInfo)
                    Log.Info("INFOR table record added " + str(upsertResult))
                else:
                    for rec in res:
                        CpqTableEntryId = rec.CpqTableEntryId
                        tableInfo = SqlHelper.GetTable("LBF_QU_INFOR_MAT_COST")
                        tablerow = { 
                                    "PARTNUMBER" : partNumber,
                                    "SITEID" : siteId,
                                    "PART_SITE_ID":str(row["PART_SITE_ID"]),
                                    "DESCRIPTION": str(row["DESCRIPTION"]),
                                    "UNIT_COST_USD": float(row["UNIT_COST_USD"]),
                                    "UNIT_PRICE_USD": float(row["UNIT_PRICE_USD"]),
                                    "WEIGHT_G": float(row["WEIGHT_G"]),
                                    "CpqTableEntryDateModified" : self.current_time,
                                    "CpqTableEntryModifiedBy" : user_info.ID,
                                    "CpqTableEntryId":CpqTableEntryId,
                                    }
                        tableInfo.AddRow(tablerow)
                        SqlHelper.Upsert(tableInfo)
                        Log.Info("INFOR table Update")
            else:
                Log.Info("Product is not there in CPQ")



#Log.Info("LBF_GS_INFOR_MATTBL_UPDATE  request---->"+str(Param))
Log.Info("LBF_GS_INFOR_MATTBL_UPDATE  request Param---->"+str(JsonHelper.Serialize(Param)))
#Log.Info("LBF_GS_INFOR_MATTBL_UPDATE  request Param.data---->"+str(JsonHelper.Serialize(Param.data)))

if (Param is not None and Param.data is not None):
    data = JsonHelper.Serialize(Param.data)
    Log.Info("LBF_GS_INFOR_MATTBL_UPDATE Param.data---->"+str(JsonHelper.Serialize(Param.data)))
    res = InforMatTblUpdate().MatUpdate(Param.data)
    ApiResponse = ApiResponseFactory.JsonResponse(res)
else:
    Log.Info('Executing...')
    ApiResponse = ApiResponseFactory.JsonResponse("Failed")