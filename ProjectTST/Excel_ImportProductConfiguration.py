end = Workbook.GetSheet("Sheet1").Cells.GetLastColumnPosition + str(Workbook.GetSheet("Sheet1").Cells.GetRowCount)
arr = Workbook.GetSheet("Sheet1").Cells.GetRange("A2", end)
container = Product.GetContainerByName("LBF_AR_CXTB_UPLOADc")
counter = 0
while counter < arr.GetLength(0):
    newRow = container.AddNewRow(True)
    newRow['PN'] = str(arr[counter,0])
    newRow['Description'] = str(arr[counter,1])
    newRow['Qty'] = str(arr[counter,2])
    newRow['Price'] = str(arr[counter,3])
    newRow['Hlit'] = str(arr[counter,4])
    newRow['ICAT'] = str(arr[counter,5])
    newRow['FD'] = str(arr[counter,6])
    counter = counter + 1
container.Calculate()