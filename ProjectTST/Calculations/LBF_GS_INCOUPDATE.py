inv_party = context.Quote.GetInvolvedParties()

ans = context.Quote.GetCustomField('LBF_CF_INCOTERMS')
res_pay = ''
res_inco = ''
for party in inv_party:
    if party.PartnerFunctionName == "Ship-to party":
        bp_id = party.BusinessPartnerId
        if bp_id:
            Log.Info('LBF_GS_INCOUPDATE if ---->')
            query = "select cf_IncoTerms, cf_PaymentTerms, BusinessPartnerId from sys_BusinessPartnerCustomFields where BusinessPartnerId = '{0}'".format(bp_id)
            bp_customField = SqlHelper.GetFirst(query)
            incoterm = bp_customField.cf_IncoTerms
            payterm = bp_customField.cf_PaymentTerms
            q1 = "select Code, [Desc] from LBF_QU_INCOTERMS where Code = '{0}'".format(incoterm)
            res = SqlHelper.GetFirst(q1)
            if res:
                res_inco = res.Desc
            q2 = "select Code, [Desc] from LBF_QU_PAYTERMS where Code = '{0}'".format(payterm)
            res2 = SqlHelper.GetFirst(q2)
            if res2:
                res_pay = res2.Desc
            # updating the incoterm and payterms custom field
            incoterm_check = context.Quote.GetCustomField("LBF_CF_INCOTERMS").Value
            payterm_check = context.Quote.GetCustomField("LBF_CF_PAYTERMS").Value

            if incoterm_check == '0' or incoterm_check == ' ' or incoterm_check == '':
                context.Quote.GetCustomField("LBF_CF_INCOTERMS").Value = res_inco
            if payterm_check == '0' or payterm_check == ' ' or payterm_check == '':
                context.Quote.GetCustomField("LBF_CF_PAYTERMS").Value = res_pay
        else:
            Log.Info('LBF_GS_INCOUPDATE else ---->')
            context.Quote.GetCustomField("LBF_CF_INCOTERMS").Value = 0
            context.Quote.GetCustomField("LBF_CF_PAYTERMS").Value = 0
            break