data = [
    {'FOB': "Shipping Point - Full Freight Allowed via truck / van to (jobsite or destination)."},
    
    {'Notes': 'Prices quoted valid for 5 days.'},
    {'Notes': 'Prices quoted do not include sales tax.'},
    {'Notes': 'Please reconfirm prices prior to placing an order.'},
    {'Shipment': 'Rail Anchors and Track Spikes - Please allow 4-6 weeks ARO for shipment.'},
    {'Shipment': 'Quoted from stock - subject to prior sale.'},
    {'Shipment': 'Tie Plates - Please allow 6-8 weeks ARO for shipment.'},
    {'Notes': 'Prices quoted are subject to base price changes in metal/steel, and rubber, fuel, scrap, energy and other surcharges in effect at time of order placement and shipment.'},
    {'Notes': 'Prices quoted valid for 5 days.'},  # duplicate
    {'Extra': 'This is a newly added section.'}
]

# Step 1: Get key order dynamically based on first appearance
key_order = []
for item in data:
    key = list(item.keys())[0]
    if key not in key_order:
        key_order.append(key)

# Step 2: Create a map for sorting keys
order_map = {key: i for i, key in enumerate(key_order)}

# Step 3: Sort by key group and then by value
sorted_data = sorted(
    data,
    key=lambda d: (order_map[list(d.keys())[0]], list(d.values())[0].lower())
)

# ✅ Print result
for item in sorted_data:
    print(item)
