import autogen

from config import AutoGen

llm_config_gpt3 = {"config_list": AutoGen.CONFIG_LIST_GPT3, "seed": 42}
llm_config_gpt4 = {"config_list": AutoGen.CONFIG_LIST_GPT4, "seed": 42}
user_proxy = autogen.UserProxyAgent(
    name="User_proxy", system_message="A human admin.", human_input_mode="TERMINATE"
)
writer = autogen.AssistantAgent(
    name="Writer",
    system_message="Writer. Your only goal is to provide high quality, detailed information on the topic given to you. You must ensure that you understand the topic and create a detailed and informative set of research on the topic. You should always reply with long, detailed research. Your research should always be structured using markdown. If you are prompted with improvements, use those improvements to improve your last set of research.",
    llm_config=llm_config_gpt3,
)
researcher = autogen.AssistantAgent(
    name="Researcher",
    system_message="Researcher. Your only goal is to provide high quality, detailed information on the topic given to you. You must ensure that you understand the topic and create a detailed and informative set of research on the topic. You should always reply with long, detailed research. Your research should always be structured using markdown. If you are prompted with improvements, use those improvements to improve your last set of research.",
    llm_config=llm_config_gpt3,
)
qa = autogen.AssistantAgent(
    name="Quality_assurance",
    system_message="Quality_assurance. You must provide quality assurance on any sets of information from the Researcher. Your goal is to ensure that information is high quality, detailed and accurate. You must also ensure that the research goes into depth enough. You must provide simple comments that will help the Researcher improve their researched information. If the information meets your requirements, you should inform the Project_manager that the information is complete and to move on. If the information is not good quality, you should inform the Researcher with the required changes.",
    llm_config=llm_config_gpt3,
)
groupchat = autogen.GroupChat(
    agents=[user_proxy, researcher], messages=[], max_round=12
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config_gpt3)
