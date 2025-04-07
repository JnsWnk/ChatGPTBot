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
        
    def submit_with_history(self, conversation_history, user_data=None):
        # Build system message with user context
        system_message = {"role": "system", "content": self._build_system_prompt(user_data)}
        
        # Combine messages (system first, then existing history)
        messages = [system_message] + conversation_history
        
        url = f"{self.basicUrl}/deployments/{self.modelName}/chat/completions/?api-version={self.apiVersion}"
        headers = {'Content-Type': 'application/json', 'api-key': self.apiKey}
        payload = {'messages': messages}
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return f"Error: {response.status_code}"
        
    def _build_system_prompt(self, user_context):
        prompt = ("You are a helpful assistant for a Telegram Chatbot. Available commands:\n"
                "/start - Begin using the bot\n"
                "/interests - Set your interests\n"
                "/help - Show help\n"
                "/match - Find people with similar interests\n"
                "/translate - Translate text\n"
                "/summarize - Summarize text\n\n"
                "General instructions: Be friendly and helpful.")
        
        if not user_context:
            return prompt
            
        prompt += "\n\nUser details:"
        if user_context.get('first_name'):
            prompt += f"\n- Name: {user_context['first_name']}"
        if user_context.get('interests'):
            prompt += f"\n- Interests: {', '.join(user_context['interests'])}"
        if user_context.get('language_code'):
            prompt += f"\n- Language: {user_context['language_code']}"
        
        return prompt + "\n\nPersonalize responses when appropriate."

if __name__ == '__main__':
    ChatGPT_test = HKBU_ChatGPT()
    while True:
        user_input = input("Typing anything to ChatGPT:\t")
        response = ChatGPT_test.submit(user_input)
        print(response)