tot_attr = Product.Attributes

for item in tot_attr:
    count = 0
    system_id = item.SystemId
    attrName = item.Name
    values = item.Values
    for value in values:
        if value.IsSelected == True:
            count += 1
            valueCode = str(value.ValueCode)
            #value = str(value.UserInput) if valueCode == "DefaultValue" else valueCode
            
            if str(self.marketId) != "8" and str(self.marketId) != "7":
                targetQtyUOM = self.Product.Attr('Target quantity UoM').GetValue()
            else:
                targetQtyUOM = ""
            #if attrName == "Target quantity UoM" and value != "EA":
            if attrName == "Number of Lengths of Rail" and targetQtyUOM != "EA":
                isShortsAllowed = self.Product.Attr('Shorts allowed?').GetValue()
                if isShortsAllowed != "Yes - Shorts Allowed":
                    calQtyUOM = self.Product.Attr('Calculated Quantity for UOM').GetValue()
                    overalLen = self.Product.Attr('Overall Length (TOTAL IN)').GetValue()
                    valueOut = (float(calQtyUOM) * 12) / float(overalLen)
                    #Log.Info("UOM: NOT EA Calculations if Value: "+str(value))
                    break

                elif isShortsAllowed == "Yes - Shorts Allowed":
                    calQtyUOM = self.Product.Attr('Calculated Quantity for UOM').GetValue()
                    perShortsAllow = self.Product.Attr('Percentage of Shorts Allowed').GetValue()
                    overalLen = self.Product.Attr('Overall Length (TOTAL IN)').GetValue()
                    assShortsLen = self.Product.Attr('Assumed Shorts Length').GetValue()
                    valueOut = (float(calQtyUOM) * 12 * (1 - (float(perShortsAllow) / 100)) / float(overalLen) ) + ((float(calQtyUOM) * (float(perShortsAllow)/100) * 12) / (float(assShortsLen) * 12))
                    #Log.Info("UOM: NOT EA Calculations elif Value: "+str(value))
                    break
                else:
                    valueOut = ""
                    #Log.Info("UOM: NOT EA Calculations else Value: "+str(value))
                    break