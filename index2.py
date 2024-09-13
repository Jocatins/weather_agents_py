import autogen

# llm_config = {"config_list": [{
#     "model": "gpt-3.5-turbo"
# }]}

llm_config_local = {"config_list" : [{
    "model": "google/gemma-2-2b",
    "base_url": "http://localhost:1234/v1",
    #  "api_key": None,
 "client":  "local" 
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