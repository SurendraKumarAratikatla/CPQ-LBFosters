from Scripting.Quote import MessageLevel


MAX_DESC_LEN = 40
EXEMPT_PART_TOKENS = ("/RMP", "/VAN", "/SAL")  # if seen (for market=7 & LBF_RAIL), skip validation

def _is_exempt_item(item):
    pn = (item.PartNumber or "").upper()
    return any(token in pn for token in EXEMPT_PART_TOKENS)

def _should_validate(market_id, user_type, items):
    """For Market 7 + LBF_RAIL: if any item is exempt, skip validation; else validate.
       For all other cases: always validate."""
    if str(market_id) == "7" and (user_type or "").strip().upper() == "LBF_RAIL":
        return not any(_is_exempt_item(i) for i in items)
    return True

def _get_desc(item):
    # Defensive read of custom attribute; coerce to string for len() safety
    try:
        val = item['LBF_QU_ITEMDESC']
    except Exception:
        val = ""
    return "" if val is None else str(val)

# --- Main -------------------------------------------------------------------
market_id = context.Quote.MarketId
user_type = getattr(User.UserType, "Name", "")

items = context.Quote.GetAllItems()
if user_type != "LBF_TTM": # If User type is LBF_TTM then no validation on length of item description text
    if not _should_validate(market_id, user_type, items):
        Trace.Write("Skipping description-length validation due to exempt part numbers.")
    else:
        too_long_parts = []
        for it in items:
            if len(_get_desc(it)) > MAX_DESC_LEN:
                val = _get_desc(it)
                it['LBF_QU_ITEMDESC'] = val[:40]
                too_long_parts.append(str(it.RolledUpQuoteItem) or "<no-part-number>")

        if too_long_parts:
            
            msg = (
            "The character limit for the field Item Description is exceeded. "
            "The field can only have a maximum of {0} characters. "
            "Affected items: {1}"
        ).format(MAX_DESC_LEN, ", ".join(too_long_parts))
            
            for msg in context.Quote.Messages:
                context.Quote.DeleteMessage(msg.Id)

            context.Quote.AddMessage(msg, MessageLevel.Error, False)
        else:
            allmsg = context.Quote.Messages
            for msg in allmsg:
                context.Quote.DeleteMessage(msg.Id)
            Log.Info("All item descriptions are within the {0}-char limit.".format(MAX_DESC_LEN))
