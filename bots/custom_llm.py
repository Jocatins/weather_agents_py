import requests

class CustomLLM:
    def __init__(self, server_url):
        self.server_url = server_url

    def chat_completion(self, prompt):
        try:
            response = requests.post(
                f'{self.server_url}/v1/chat/completions',
                json={
                    "model": "gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
                    'messages': [{'role': 'user', 'content': prompt}]
                }
            )
            response_json = response.json()
            print("Response JSON:", response_json)
            if 'choices' in response_json:
                return response_json['choices'][0]['message']['content']
            else:
                return f"Error: Unexpected response structure: {response_json}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"
