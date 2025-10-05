from LBF_GS_CREATEBEARERTOKEN import creating_bearer_token
# import clr
clr.AddReference('Newtonsoft.Json')
from Newtonsoft.Json import JsonConvert
from Newtonsoft.Json.Linq import JObject

response = creating_bearer_token()
if response[1] == 'success':
    stream = RestClient.DeserializeJson(StreamReader(response[0].GetResponseStream()).ReadToEnd())
    bearer_token = stream.access_token

url = 'https://lbfoster-tst.cpq.cloud.sap/api/v1/quotes/{}'.format('521')
encodedKeys = "Bearer "+str(bearer_token)
headers = {"Authorization":encodedKeys}
quoteHeaderObj = RestClient.Get(url, headers)
serialized_data = JsonConvert.SerializeObject(quoteHeaderObj)