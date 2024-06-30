import http.client
import json

def send_sms(user):
  conn = http.client.HTTPSConnection("rgegpp.api.infobip.com")
  payload = json.dumps({
      "messages": [
          {
              "destinations": [{"to":"254701948782"}],
              # "destinations": [{"to": "254" + str(user.phone)}],
              "from": "ServiceSMS",
              "text": "CONGRATULATIONS! You have been MATCHED successfully, please login to 'https://iswapp.pythonanywhere.com' to view details about your swapmate!"
          }
      ]
  })
  headers = {
      'Authorization': 'App 280d116f8a80907df1652d4170fb0840-d67476a0-f931-4918-829c-5fb0d13db617',
      'Content-Type': 'application/json',
      'Accept': 'application/json'
  }
  conn.request("POST", "/sms/2/text/advanced", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8")) 