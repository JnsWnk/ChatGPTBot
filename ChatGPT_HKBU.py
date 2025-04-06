import configparser
import requests

class HKBU_ChatGPT():
    def __init__(self, c_api):
        self.apiKey = c_api
        self.basicUrl = "https://genai.hkbu.edu.hk/general/rest"
        self.modelName = "gpt-4-o-mini"
        self.apiVersion = "2024-10-21"
    def submit(self,message):
        conversation = [{"role": "user", "content": message}]
        url = self.basicUrl + "/deployments/" +self. modelName + "/chat/completions/?api-version=" + self.apiVersion
        headers = { 'Content-Type': 'application/json', 'api-key': self.apiKey }
        payload = { 'messages': conversation }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:', response

if __name__ == '__main__':
    ChatGPT_test = HKBU_ChatGPT()
    while True:
        user_input = input("Typing anything to ChatGPT:\t")
        response = ChatGPT_test.submit(user_input)
        print(response)