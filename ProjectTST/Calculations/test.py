def ascii_code_validation():
    for item in context.Quote.GetAllItems():
        if item["LBF_QU_Notes"] or item["LBF_QU_ITEMDESC"]:
            Trace.Write(item["LBF_QU_Notes"])
            item["LBF_QU_Notes"] = item["LBF_QU_Notes"].replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace("–","–").replace("—","—")
            item["LBF_QU_ITEMDESC"] = item["LBF_QU_ITEMDESC"].replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace("–","–").replace("—","—")
        else:
            continue
ascii_code_validation()