Number of Lengths of Rail = (Calculated Quantity for UOM * 12) / Overall Length (TOTAL IN) 

IF Shorts allowed = 'N' and Target quantity UoM not equal to 'EA',

Number of Lengths of Rail = (Calculated Quantity for UOM * 12 * (1-(Percentage of Shorts Allowed /100))/  Overall Length (TOTAL IN)) + 
((Calculated Quantity for UOM * (Percentage of Shorts Allowed / 100) * 12) / (Assumed Shorts Length * 12)) 
IF Assumed Shorts Length= 'Y' and and Target quantity UoM not equal to 'EA'

targetQtyUOM = self.Product.Attr('Target quantity UoM').GetValue()
if attrName == "Number of Lengths of Rail" and targetQtyUOM != "EA":
    isShortsAllowed = Product.Attr('Shorts allowed?').GetValue()
    if isShortsAllowed != "Yes - Shorts Allowed":
        calQtyUOM = Product.Attr('Calculated Quantity for UOM').GetValue()
        overalLen = Product.Attr('Overall Length (TOTAL IN)').GetValue()
        value = (float(calQtyUOM) * 12) / float(overalLen)

    elif isShortsAllowed == "Yes - Shorts Allowed":
        calQtyUOM = Product.Attr('Calculated Quantity for UOM').GetValue()
        perShortsAllow = Product.Attr('Percentage of Shorts Allowed').GetValue()
        overalLen = Product.Attr('Overall Length (TOTAL IN)').GetValue()
        assShortsLen = Product.Attr('Assumed Shorts Length').GetValue()
        value = (float(calQtyUOM) * 12 * (1 - (float(perShortsAllow) / 100)) / float(overalLen) ) + ((float(calQtyUOM) * (float(perShortsAllow)/100) * 12) / float(assShortsLen) * 12)