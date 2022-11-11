import requests, uuid, json

# Add your key and endpoint
key = "121f98c34ffa4c67992f82a1659ec0df"
endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "centralindia"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'zh',
    'to': ['en']
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}
x = '1999 年 1 月 19 日'
y = '男性, 女性, 一亿九千九百二十三万四千五百三十二'
# You can pass more than one object in body.
body = [{'text': y},
         {'text': x}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()

print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=2, separators=(',', ': ')))
# x = json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
# print(response[0]['translations'][0]['text'])
# print(response)