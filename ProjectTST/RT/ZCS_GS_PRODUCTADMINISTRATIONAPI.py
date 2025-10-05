from ZCS_GS_CREATEBEARERTOKEN import creating_bearer_token

def SimpleProductAdministrationAPI():
    fullResultSet = []
    batch_size=500
    countCheckQuery = SqlHelper.GetFirst("select count(CpqTableEntryId) as cnt from ZCS_CPQ_PRODUCT_MASTER(NOLOCK) where MaterialNumber != '' AND Description !='' AND MaterialType ='ZFER'")
    if countCheckQuery is not None:
        count=int(countCheckQuery.cnt)
        for offset in xrange(0, count, batch_size):
            resultSet=[]
            # resultSet = SqlHelper.GetList("Select MaterialType as Finished_goods,MaterialNumber as Product_Id,ProductHierarchy as Category,Description as Product_Name,ProductType as Product_Type from ZCS_CPQ_PRODUCT_MASTER where MaterialNumber != '' AND Description !='' AND MaterialType ='ZFER' order by (SELECT NULL) OFFSET "+str(offset)+"  ROWS FETCH NEXT "+str(batch_size)+" ROWS ONLY")
            resultSet = SqlHelper.GetList("SELECT distinct pm.MaterialNumber as Product_Id,pm.ProductHierarchyString as Category,pm.Description as Product_Name,pm.ProductType as Product_Type,p.PRODUCT_ID as prdId FROM ZCS_CPQ_PRODUCT_MASTER pm join Products p on p.Product_catalog_code = pm. MaterialNumber left outer join PRODUCT_ATTRIBUTES pa on pa.product_id = p.PRODUCT_ID where pa.PA_ID is null and pm.MaterialType = 'ZFER' and pm.MaterialNumber != '' AND pm.Description !='' AND p.PRODUCT_ACTIVE='1' order by pm.MaterialNumber,pm.ProductHierarchyString,pm.Description,pm.ProductType OFFSET "+str(offset)+"  ROWS FETCH NEXT "+str(batch_size)+" ROWS ONLY")
            for  datarow in resultSet:
                fullResultSet.append(datarow)
        Trace.Write(len(fullResultSet))
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT Username,Password,Domain FROM ZCS_CPQ_INTEGRATION_USER (NOLOCK)")
    if LOGIN_CREDENTIALS is not None:
        Login_Username = str(LOGIN_CREDENTIALS.Username)
        Login_Password = str(LOGIN_CREDENTIALS.Password)
        Login_Domain = str(LOGIN_CREDENTIALS.Domain)
    ws = WebServiceHelper.Load("https://electroitsolab-tst.cpq.cloud.sap/wsAPI/wssrv.asmx")
    username = str(Login_Username) + "#" + str(Login_Domain)
    password = str(Login_Password)
    Value = tabContent = ''
    Action = "ADDORUPDATE"
    ProductName = Categories = data =''
    a_dict = {}
    for i in fullResultSet:
        #Trace.Write('111111111111111')
        ProductName = i.Product_Name.replace("&", "&amp;")
        CPQProductID = str(i.Product_Id)
        PartNumber = str(i.Product_Id)
        ProductType = str(i.Product_Type)
        Categories = str(i.Category).replace("&", "&amp;")
        Product_Id = str(i.prdId)
        '''Trace.Write('ProductName.....'+str(ProductName))
        Trace.Write('CPQProductID.....'+str(CPQProductID))
        Trace.Write('PartNumber.....'+str(PartNumber))
        Trace.Write('ProductType.....'+str(ProductType))
        Trace.Write('Categories.....'+str(Categories))'''
        APIdata = "<?xml version='1.0' encoding='utf-8'?><Products><Product><CPQProductID>" + str(CPQProductID) + "</CPQProductID><PartNumber>" + str(PartNumber)+ "</PartNumber><DisplayType>Configurable</DisplayType>"
        APIdata += "<Active>true</Active><ProductType>"+str(ProductType)+"</ProductType><ProductName><USEnglish>"+ ProductName +"</USEnglish></ProductName><Categories><USEnglish>"+ str(Categories) + "</USEnglish></Categories>"
        
        Value +="<Attribute><AttributeName><USEnglish><![CDATA[Accessories]]></USEnglish></AttributeName><AttributeSystemId>Accessories_cpq</AttributeSystemId><AttributeType>Container</AttributeType><DisplayType>Container</DisplayType><Label>Accessories</Label><IsLineItem>0</IsLineItem><Values><Value><USEnglish><![CDATA[1]]></USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
        Value += "<Attribute><AttributeName><USEnglish><![CDATA[Services]]></USEnglish></AttributeName><AttributeSystemId>Services_cpq</AttributeSystemId><AttributeType>Container</AttributeType><DisplayType>Container</DisplayType><Label>Services</Label><IsLineItem>0</IsLineItem><Values><Value><USEnglish><![CDATA[1]]></USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
        Value += "<Attribute><AttributeName><USEnglish><![CDATA[ZCS_AR_ChildContainer]]></USEnglish></AttributeName><AttributeSystemId>ZCS_AR_ChildContainer_cpq</AttributeSystemId><AttributeType>Container</AttributeType><DisplayType>Container</DisplayType><Label>ZCS_AR_ChildContainer</Label><IsLineItem>1</IsLineItem><Values><Value><USEnglish><![CDATA[1]]></USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
        tabContent = "<Tab><SystemId>AccessoriesTab_cpq</SystemId><Name>Accessories</Name><Rank>10</Rank> <LayoutTemplate>Standard - 1 Column</LayoutTemplate> <VisibilityPermission>2</VisibilityPermission> <VisibilityCondition>1</VisibilityCondition> <ShowTabHeader>1</ShowTabHeader> <Attributes> <Attribute> <Name>Accessories</Name> <Rank>10</Rank> </Attribute> </Attributes></Tab><Tab><SystemId>ServicesTab_cpq</SystemId><Name>Services</Name><Rank>10</Rank> <LayoutTemplate>Standard - 1 Column</LayoutTemplate> <VisibilityPermission>2</VisibilityPermission> <VisibilityCondition>1</VisibilityCondition> <ShowTabHeader>1</ShowTabHeader> <Attributes> <Attribute><Name>Services</Name> <Rank>20</Rank></Attribute> </Attributes></Tab>"
        APIdata += "<Attributes>" + Value + "</Attributes>"
        # APIdata += "<Tabs>"+tabContent+"</Tabs><GlobalScripts><Script><Name>ZCS_GS_ACCESSORIESDATA</Name><Rank>10</Rank><Events><Event>OnProductLoaded</Event></Events></Script><Script><Name>ZCS_GS_SERVICESDATA</Name><Rank>10</Rank><Events><Event>OnProductLoaded</Event></Events></Script></GlobalScripts></Product></Products>"
        APIdata += "<Tabs>"+tabContent+"</Tabs></Product></Products>"
        #Log.Info('APIdata..'+APIdata)
        data = XmlHelper.Load(APIdata)
        f = ws.SimpleProductAdministration(username, password, Action, data)
        a_dict[str(PartNumber)] = str(f.Message)
        response,token_msg = creating_bearer_token()
        if token_msg == "success":
            accessToken = (RestClient.DeserializeJson(StreamReader(response.GetResponseStream()).ReadToEnd())).access_token
        elif token_msg == "error":
            errorData = StreamReader(errorResponse.GetResponseStream())
            reader = errorData.ReadToEnd()
            errorData.Close()
            errorToJson = RestClient.SerializeToJson(reader)
        attrCodeQuery = SqlHelper.GetFirst("select STANDARD_ATTRIBUTE_CODE from PRODUCT_ATTRIBUTES where PRODUCT_ID ='"+ str(Product_Id) +"' AND LINEITEM='1'")
        if attrCodeQuery is not None:
            attrCode = attrCodeQuery.STANDARD_ATTRIBUTE_CODE
        else:
            attrCode =''
        if attrCode:
            baseURL = "https://electroitsolab-tst.cpq.cloud.sap"
            encodedKeys = "Bearer "+str(accessToken)
            headers = {"Authorization":encodedKeys}
            request = baseURL + "/setup/api/v1/admin/products/"+Product_Id+"/attributes/"+str(attrCode)
            #Log.Info("REQUEST---------"+str(request))
            responseJson=RestClient.Get(request,headers)
            if responseJson.lineItemInfo.expCanEnterQty == "0":
                responseJson.lineItemInfo.expCanEnterQty = "1"
            t = (RestClient.SerializeToJson(responseJson))


            endpointURL = baseURL +"/setup/api/v1/admin/products/productAttributes"
            response = RestClient.Post(endpointURL, t, headers)

    Trace.Write('------------------------------------------------------------'+str(a_dict))
    return '1'
ApiResponse = ApiResponseFactory.JsonResponse(SimpleProductAdministrationAPI())