import os
import autogen
from autogen import AssistantAgent, UserProxyAgent

os.environ["OPENAI_API_KEY"] = "dummy_key"  # Ensure this key doesn't cause issues

llm_config_local = {"config_list": [{
    "model": "gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
    "base_url": "http://localhost:1234/v1/completions",
    "api_key": None,  # You might not need this for a local model
    "price": [0, 0]
}]}

# Initialize the assistant
assistant = AssistantAgent("assistant", llm_config=llm_config_local)
if assistant is None:
    print("AssistantAgent failed to initialize.")

# Initialize the user proxy
user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")}
)

# Debugging the initialization
if user_proxy is None:
    print("UserProxyAgent failed to initialize.")
else:
    print("UserProxyAgent initialized successfully.")

# Start the chat
try:
    user_proxy.initiate_chat(
        assistant,
        message="Plot a chart of NVDA and TESLA stock price change YTD.",
    )
except Exception as e:
    print(f"Error during chat initiation: {e}")
