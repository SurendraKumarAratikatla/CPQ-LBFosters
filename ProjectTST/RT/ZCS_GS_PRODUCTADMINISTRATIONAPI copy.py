def SimpleProductAdministrationAPI():
    ws = WebServiceHelper.Load("http://lbfoster-tst.cpq.cloud.sap/wsAPI/wssrv.asmx")
    username = 'Surendra.aratikatla@knacksystems.com'
    password = 'Surendra@31'
    Action = "ADDORUPDATE"
    APIdata = "<Products><Product><Identificator>ProductSystemId</Identificator><ProductSystemId>000000000000011106</ProductSystemId><PartNumber>11106</PartNumber><ProductType>01100303</ProductType><IsSyncedFromBackOffice>False</IsSyncedFromBackOffice><UnitOfMeasure>FOT</UnitOfMeasure><Categories><USEnglish>LB005</USEnglish></Categories><ProductName><USEnglish>NEW 12AS RAIL, ENDS DRILLED 2 X 4</USEnglish></ProductName><SalesUnitsOfMeasure><SalesUnitOfMeasure><Unit>EA</Unit><Denominator>1</Denominator><Numerator>40</Numerator></SalesUnitOfMeasure><SalesUnitOfMeasure><Unit>LBR</Unit><Denominator>400</Denominator><Numerator>100</Numerator></SalesUnitOfMeasure></SalesUnitsOfMeasure></Product></Products>"
    data = XmlHelper.Load(APIdata)
    f = ws.SimpleProductAdministration(username, password, Action, data)
SimpleProductAdministrationAPI()



def SimpleProductAdministrationAPI():
    ws = WebServiceHelper.Load("http://lbfoster-tst.cpq.cloud.sap/wsAPI/wssrv.asmx")
    username = 'Surendra.aratikatla@knacksystems.com'
    password = 'Surendra@31'
    Action = "ADDORUPDATE"
    APIdata = "<Products><Product><Identificator>ProductSystemId</Identificator><ProductSystemId>TEST_PRODUCT4_cpq</ProductSystemId><PartNumber>10001</PartNumber><ProductType>01100303</ProductType><IsSyncedFromBackOffice>False</IsSyncedFromBackOffice><UnitOfMeasure>FOT</UnitOfMeasure><Categories><USEnglish>LB Foster>Rail>FMSA</USEnglish></Categories><ProductName><USEnglish>TEST PRODUCT4</USEnglish></ProductName><SalesUnitsOfMeasure><SalesUnitOfMeasure><Unit>EA</Unit><Denominator>1</Denominator><Numerator>40</Numerator></SalesUnitOfMeasure><SalesUnitOfMeasure><Unit>LBR</Unit><Denominator>400</Denominator><Numerator>100</Numerator></SalesUnitOfMeasure></SalesUnitsOfMeasure></Product></Products>"
    data = XmlHelper.Load(APIdata)
    f = ws.SimpleProductAdministration(username, password, Action, data)
SimpleProductAdministrationAPI()




def SimpleProductAdministrationAPI():
    ws = WebServiceHelper.Load("http://lbfoster-tst.cpq.cloud.sap/wsAPI/wssrv.asmx")
    username = 'Surendra.aratikatla@knacksystems.com'
    password = 'Surendra@31'
    Action = "ADDORUPDATE"
    APIdata = "<Products><Product><Identificator>ProductSystemId</Identificator><ProductSystemId>TEST_PRODUCT5_cpq</ProductSystemId><PartNumber>HH_NEW_T_RAIL</PartNumber><ProductType>01100303</ProductType><IsSyncedFromBackOffice>False</IsSyncedFromBackOffice><UnitOfMeasure>FOT</UnitOfMeasure><Categories><USEnglish>LB Foster>Rail>FMSA</USEnglish></Categories><ProductName><USEnglish>Head Harened Configurable Rail</USEnglish></ProductName><SalesUnitsOfMeasure><SalesUnitOfMeasure><Unit>FOT</Unit><Denominator>1</Denominator><Numerator>40</Numerator></SalesUnitOfMeasure><SalesUnitOfMeasure><Unit>LBR</Unit><Denominator>400</Denominator><Numerator>100</Numerator></SalesUnitOfMeasure></SalesUnitsOfMeasure></Product></Products>"
    data = XmlHelper.Load(APIdata)
    f = ws.SimpleProductAdministration(username, password, Action, data)
SimpleProductAdministrationAPI()