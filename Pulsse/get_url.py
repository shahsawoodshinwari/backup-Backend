import requests

def getting_url():
    def get_key():
        response = requests.post('https://open.ezvizlife.com/api/lapp/token/get', 
                                headers={"Content-Type": "application/x-www-form-urlencoded"},
                                data={"appKey": "fc2c7d28d761409ca6c2a1340490cd12",
                                    "appSecret": "ed8d3fbe7316413b90fdf00df9c13c01"}
                                )

        if response.status_code == 200:
            return response.json()["data"]["accessToken"]
        else:
            return ""
        
    def get_feed_url(accessToken, deviceSerial, code=654321, expireTime=90000, channelNo=1, protocol=2):
        response = requests.post('https://isgpopen.ezvizlife.com/api/lapp/live/address/get', 
                                headers={"Content-Type": "application/x-www-form-urlencoded"},
                                data={"accessToken": accessToken,
                                    "deviceSerial": deviceSerial,
                                    "code": code,
                                    "expireTime": expireTime,
                                    "channelNo": channelNo,
                                    "protocol": protocol,
                                    }
                                )
        
        if response.status_code == 200:
            return response.json()["data"]["url"]
        else:
            return ""

    accessToken = get_key()
    # print(f"Access Token: {accessToken}")

    url1 = get_feed_url(accessToken, "AB9438217")
    # print(f"url1: {url1}")

    url2 = get_feed_url(accessToken, "AA4823505")
    # print(f"url2: {url2}")

    return {"url1": url1, "url2": url2}

# # Usage example:
# urls = getting_url()
# print("url1:", urls["url1"])
# print("url2:", urls["url2"])
