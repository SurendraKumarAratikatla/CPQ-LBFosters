from System.Text import Encoding
from System.Net import WebRequest
from System.Net import WebException

def creating_bearer_token():
    #User_Details = SqlHelper.GetFirst("select * from LBF_QU_CREDENTIALS_TBL where UserName = 'lakshya.srivastava@knacksystems.com'")
    User_Details = SqlHelper.GetFirst("select * from LBF_QU_CREDENTIALS_TBL")
    data = Encoding.UTF8.GetBytes("grant_type=password&username="+str(User_Details.UserName)+"&password="+str(User_Details.Password)+"&domain="+str(User_Details.Domain))
    #Trace.Write(data)
    # Create a request using a URL that can receive a post.
    request = WebRequest.Create("https://lbfoster-tst.cpq.cloud.sap/basic/api/token");
    request.Method = "POST";

    # Set the ContentType property of the WebRequest.
    request.ContentType = "application/x-www-form-urlencoded";
    request.Accept = 'application/json'
    request.ContentLength = data.Length
    request.GetRequestStream().Write(data, 0, data.Length);

    try:
        response = request.GetResponse()
        #stream = RestClient.DeserializeJson(StreamReader(response.GetResponseStream()).ReadToEnd())
        #bearer_token = stream.access_token
        return response,"success"

    except WebException, we:
        errorResponse = we.Response
        #errorData = StreamReader(errorResponse.GetResponseStream())
        #errorToJson = errorData.ReadToEnd()
        return errorResponse,"fail"