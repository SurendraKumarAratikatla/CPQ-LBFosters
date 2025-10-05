class InforMat():
    def __init__(self):
        self.quoteInfo = context.Quote
    def PriceCostUpdate(self):
        #for item in context.AffectedItems:
        for item in context.Quote.GetAllItems():
            proSystemId = item.ProductSystemId
            site = proSystemId[-3:]
            inforData = SqlHelper.GetFirst("select PART_SITE_ID,UNIT_COST_USD,UNIT_PRICE_USD from LBF_QU_INFOR_MAT_COST where PART_SITE_ID = '{0}'".format(proSystemId))
            #Cost and price available in LBF_QU_INFOR_MAT_COST
            if inforData:
                Trace.Write('LBF_QC_InforMatCheck ran')
                item['LBF_QU_NetWeight'] = str(1)
                item['LBF_QU_FM_PLANT'] = str(site)
                if site == "RMP":
                    item['LBF_QU_Currency'] = "USD"
                    customfield = context.Quote.GetCustomField('LBF_CF_Address')
                    customfield.Value = str('''L.B. Foster Rail Technologies, Inc.
                                            415 Holiday Dr.
                                            Pittsburgh, PA 15220 ''')
                    # MAT COST currency as USD
                    query_currencies = SqlHelper.GetFirst("Select CURRENCY, QUOTE from CURRENCIES WHERE CURRENCY ='{0}'".format(item['LBF_QU_Currency']))
                    item['LBF_QU_MAT_CST'] = str(query_currencies.QUOTE)
                    Trace.Write('in if...'+str(str(float(item['LBF_QU_MAT_CST'])*float(query_currencies.QUOTE))))
                    Trace.Write(item.PartNumber)
                    Trace.Write("------------------------")

                    
            	elif site == "VAN":
                    item['LBF_QU_Currency'] = "CAD"
                    customfield = context.Quote.GetCustomField('LBF_CF_Address')
                    customfield.Value = str('''L.B. Foster Rail Technologies Corp.
                                               4041 Remi Place Burnaby,
                                               B.C. Canada V5A 4J8''')
                    # MAT COST currency conversion from USD to CAD from Currencies
                    query_currencies = SqlHelper.GetFirst("Select CURRENCY, QUOTE from CURRENCIES WHERE CURRENCY ='{0}'".format(item['LBF_QU_Currency']))
                    item['LBF_QU_MAT_CST'] = str(float(item['LBF_QU_MAT_CST'])*float(query_currencies.QUOTE))
                    Trace.Write('in else...'+str(str(float(item['LBF_QU_MAT_CST'])*float(query_currencies.QUOTE))))
                    Trace.Write(item.PartNumber)
                    Trace.Write("------------------------")


                    
                item['LBF_QU_PLANT1'] = str("N/A")
                item['LBF_QU_ITEMDESC'] = item.Description if item.Description else ""
                item['LBF_QU_FREIGHT_CST_EXT'] = item['LBF_QU_HANDLING_CST_EXT'] = str(0)
                quantity = float(item.Quantity)
                cost = round(float(inforData.UNIT_COST_USD),2)
                #Trace.Write(cost)
                if cost != 0.00:
                    item['LBF_QU_MAT_CST'] = str(round(float(inforData.UNIT_COST_USD),2))
                    ext_cost = float(item['LBF_QU_MAT_CST']) * quantity if quantity != 0 else 0.0
                    item['LBF_QU_ExtCost'] = str(round(ext_cost, 2))
                    item['LBF_QU_HANDLING_OB'] = "MAN"
                    total_cost = float(item['LBF_QU_FREIGHT_CST_EXT']) + float(item['LBF_QU_HANDLING_CST_EXT']) + float(item['LBF_QU_ExtCost'])
                    item['LBF_QU_TOTAL_COST'] = str(round(float(total_cost),2))
                    selling_price = round(float(inforData.UNIT_PRICE_USD))
                    if selling_price != 0.00:
                        item['LBF_QU_SELPRICE_UN'] = str(round(float(selling_price),2))
                        item['LBF_QU_SELPRICE'] = total_price = str(round((float(selling_price) * quantity), 2))
                        # Trace.Write(total_price)
                        gross_profit_percent = ((float(total_price) - float(total_cost)) / float(total_price)) * 100
                        item['LBF_QU_GP_PER'] = str(gross_profit_percent)
                        gross_profit_value = (float(total_price) - float(total_cost)) * quantity
                        item['LBF_QU_GP_VAL'] = str(round(gross_profit_value, 2))
                        Log.Info(str(selling_price))
    def run(self):
        self.PriceCostUpdate()


object = InforMat().run()