import os
import json
import autogen

GPT35 = "gpt-3.5-turbo-1106"
GPT4 = "gpt-4-1106-preview"

os.environ["OAI_CONFIG_LIST"] = json.dumps(
    [
        {
            "model": GPT35,
            "api_key": os.environ["OPENAI_API_KEY"],
        },
        {
            "model": GPT4,
            "api_key": os.environ["OPENAI_API_KEY"],
        },
    ]
)


class EnabledModels:
    WRITING = GPT35
    HEADINGS = GPT35
    ICONS = GPT35


class AutoGen:
    CONFIG_LIST_GPT3 = autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST", filter_dict={"model": [GPT35]}
    )

    CONFIG_LIST_GPT4 = autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST", filter_dict={"model": [GPT4]}
    )
