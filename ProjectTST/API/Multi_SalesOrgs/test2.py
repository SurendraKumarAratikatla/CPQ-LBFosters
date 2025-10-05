from collections import OrderedDict

requestData = OrderedDict({
    'Root': OrderedDict({
        "QuoteItems": 'quoteData',
        "QuoteHeader": 'q'
    })
})

print(requestData)
