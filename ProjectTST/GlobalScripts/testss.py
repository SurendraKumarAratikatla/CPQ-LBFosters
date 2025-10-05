sku_code = ''
plant = ''
new_row_data = {}

for row in Product.GetContainerByName('PPK_AR_Selected_ProductSKU').Rows:
    sku_code = row['SKU_Code']
    plant = row['Production_Plant']

Log.Info("Material_Number")
changesCell = EventArgs.ChangedCell
if changesCell.ColumnName == "Material_Number":
    # getting packaging BOM

    rowIndex = changesCell.RowIndex
    row = Product.GetContainerByName('PPK_AR_PackagingBOM').Rows[rowIndex]

    material_number = row['Material_Number']
    Log.Info(material_number)
    Log.Info("In Packaging bom")
    query = "SELECT Max(NetOrder_Price) as netPrice FROM PPK_PD_PURCHASEPRICEHISTORY WHERE Material = '{0}' and Price_Unit = '1000'".format(material_number)
    price = SqlHelper.GetFirst(query)

    # First query with FG_Material and Plant
    sql_query = """
    SELECT Material, Material_Description, Turn, Plant, FG_Material, Price_Per_M, Quantity, UOM, Material_Type
    FROM PPK_PD_PACKAGINGBOM
    WHERE Material = '{}' AND FG_Material = '{}' AND Plant = '{}'
    """.format(material_number, sku_code, plant)

    row_data = SqlHelper.GetFirst(sql_query)
    Log.Info("old")
    Log.Info(str(row_data))
    if row_data is None:
        # Second query with only Material
        sql_query = """
        SELECT Material, Material_Description, Turn, Plant, FG_Material, Price_Per_M, Quantity, UOM, Material_Type
        FROM PPK_PD_PACKAGINGBOM
        WHERE Material = '{}'
        """.format(material_number)

        new_row_data = SqlHelper.GetFirst(sql_query)
        Log.Info("new")
        Log.Info(str(new_row_data))
        Log.Info(str(new_row_data.Material_Description))
        if new_row_data is not None:
            row.Product.Attr('PPK_AR_PACK_ID').AssignValue(new_row_data.Material)
            row['Temp_Part_Number'] = new_row_data.Material
            row.Product.Attr('PPK_AR_PACK_DECS').AssignValue(new_row_data.Material_Description)
            row['Material_Description'] = str(new_row_data.Material_Description)
            #row['Material_Description'] = AssignValue(str(new_row_data.Material_Description))
            #row['Material_Description'] = SelectDisplayValue(str(new_row_data.Material_Description))
            row['UOM'] = new_row_data.UOM
            row['Material_Type'] = new_row_data.Material_Type
            #row['Cost_Per_1000'] = ''  # Assuming no cost per 1000 data to update
            row['Turn'] = new_row_data.Turn  # Assuming no turn data to update
            row['Qty'] = str(new_row_data.Quantity)
            row.Product.Attr('ItemQuantity').AssignValue(str(new_row_data.Quantity))
            if price:
                row['Cost_Per_1000'] = str(price.netPrice)
            row.ApplyProductChanges()
    else:
        row.Product.Attr('PPK_AR_PACK_ID').AssignValue(row_data.Material)
        row['Temp_Part_Number'] = row_data.Material
        row.Product.Attr('PPK_AR_PACK_DECS').AssignValue(row_data.Material_Description)
        row['Material_Description'] = str(row_data.Material_Description)
        #row['Material_Description'] = AssignValue(str(new_row_data.Material_Description))
        #row['Material_Description'] = SelectDisplayValue(str(new_row_data.Material_Description))
        Log.Info(str(new_row_data.Material_Description))
        row['UOM'] = row_data.UOM
        row['Material_Type'] = row_data.Material_Type
        #row['Cost_Per_1000'] = ''  # Assuming no cost per 1000 data to update
        row['Turn'] = row_data.Turn  # Assuming no turn data to update
        row['Qty'] = str(row_data.Quantity)
        row.Product.Attr('ItemQuantity').AssignValue(str(new_row_data.Quantity))
        if price:
            row['Cost_Per_1000'] = str(price.netPrice)
        row.ApplyProductChanges()


#Material_Description

if changesCell.ColumnName == "Material_Description":
    # getting packaging BOM

    rowIndex = changesCell.RowIndex
    row = Product.GetContainerByName('PPK_AR_PackagingBOM').Rows[rowIndex]

    material_dec = row['Material_Description']
    Log.Info(material_dec)
    Log.Info("In Packaging bom dec")
    query = "SELECT Max(NetOrder_Price) as netPrice FROM PPK_PD_PURCHASEPRICEHISTORY WHERE Material_Description = '{0}' and Price_Unit = '1000'".format(material_dec)
    price = SqlHelper.GetFirst(query)

    # First query with FG_Material and Plant
    sql_query = """
    SELECT Material, Material_Description, Turn, Plant, FG_Material, Price_Per_M, Quantity, UOM, Material_Type
    FROM PPK_PD_PACKAGINGBOM
    WHERE Material_Description = '{}' AND FG_Material = '{}' AND Plant = '{}'
    """.format(material_dec, sku_code, plant)

    row_data = SqlHelper.GetFirst(sql_query)
    Log.Info("old")
    Log.Info(str(row_data))
    if row_data is None:
        # Second query with only Material
        sql_query = """
        SELECT Material, Material_Description, Turn, Plant, FG_Material, Price_Per_M, Quantity, UOM, Material_Type
        FROM PPK_PD_PACKAGINGBOM
        WHERE Material_Description = '{}'
        """.format(material_dec)

        new_row_data = SqlHelper.GetFirst(sql_query)
        Log.Info("new")
        Log.Info(str(new_row_data))
        if new_row_data is not None:
            row.Product.Attr('PPK_AR_PACK_ID').AssignValue(new_row_data.Material)
            row['Temp_Part_Number'] = new_row_data.Material
            row.Product.Attr('PPK_AR_PACK_DECS').AssignValue(new_row_data.Material_Description)
            #row['Material_Description'] = new_row_data.Material_Description
            row['Material_Number'] = new_row_data.Material
            row['UOM'] = new_row_data.UOM
            row['Material_Type'] = new_row_data.Material_Type
            #row['Cost_Per_1000'] = ''  # Assuming no cost per 1000 data to update
            row['Turn'] = new_row_data.Turn  # Assuming no turn data to update
            row['Qty'] = str(new_row_data.Quantity)
            row.Product.Attr('ItemQuantity').AssignValue(str(new_row_data.Quantity))
            if price:
                row['Cost_Per_1000'] = str(price.netPrice)
            row.ApplyProductChanges()
    else:
        row.Product.Attr('PPK_AR_PACK_ID').AssignValue(row_data.Material)
        row['Temp_Part_Number'] = row_data.Material
        row.Product.Attr('PPK_AR_PACK_DECS').AssignValue(row_data.Material_Description)
        #row['Material_Description'] = row_data.Material_Description
        row['Material_Number'] = new_row_data.Material
        row['UOM'] = row_data.UOM
        row['Material_Type'] = row_data.Material_Type
        #row['Cost_Per_1000'] = ''  # Assuming no cost per 1000 data to update
        row['Turn'] = row_data.Turn  # Assuming no turn data to update
        row['Qty'] = str(row_data.Quantity)
        row.Product.Attr('ItemQuantity').AssignValue(str(new_row_data.Quantity))
        if price:
            row['Cost_Per_1000'] = str(price.netPrice)
        row.ApplyProductChanges()