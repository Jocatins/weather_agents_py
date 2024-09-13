import autogen
import os

os.environ["OPENAI_API_KEY"] = "dummy_key"


llm_config_local = {"config_list" : [{
    "model": "gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
    "base_url": "http://localhost:1234/v1/completions",
     "api_key": None,
     "price": [0, 0]
}],
}

nico = autogen.AssistantAgent(
    name="nico",
    system_message="Telling Jokes",
    llm_config=llm_config_local
)

karla = autogen.AssistantAgent(
    name="karla",
    system_message="Criticize Jokes",
    llm_config=llm_config_local
)

def termination_message(msg):
    return "TERMINATE" in str(msg.get("content", ""))

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    code_execution_config={"use_docker": False},
    is_termination_msg=termination_message,
    human_input_mode="NEVER"
)

groupchat = autogen.GroupChat(
    agents=[nico, karla, user_proxy],
    messages=[],
    speaker_selection_method="round_robin"
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    code_execution_config = {"use_docker": False},
    llm_config=llm_config_local,
    is_termination_msg = termination_message
)

user_proxy.initiate_chat(
    manager,
    message="Tell a joke"
)