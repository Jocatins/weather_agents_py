import os
import autogen
from autogen import AssistantAgent, UserProxyAgent 

os.environ["OPENAI_API_KEY"] = "dummy_key"

llm_config_local = {"config_list": [{
    "model": "gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
    "base_url": "http://localhost:1234/v1/completions",
    "api_key": None,
    "price": [0, 0]
}]}

# Initialize the assistant
assistant = AssistantAgent("assistant", llm_config=llm_config_local)
if assistant is None:
    print("AssistantAgent failed to initialize.")
else:
    print("AssistantAgent initialized successfully.")

# Test direct communication with the AssistantAgent
try:
    assistant_response = assistant.run(message="Plot a chart of NVDA and TESLA stock price change YTD.")
    print(f"Assistant response: {assistant_response}")
except Exception as e:
    print(f"Error during direct communication: {e}")

# Initialize the user proxy
user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")}
)

# Start the chat
try:
    user_proxy.initiate_chat(
        assistant,
        message="Plot a chart of NVDA and TESLA stock price change YTD.",
    )
except Exception as e:
    print(f"Error during chat initiation: {e}")
