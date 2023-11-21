import os
import json
import autogen

GPT35 = "gpt-3.5-turbo"
GPT4 = "gpt-4-1106-preview"


class AutoGen:
    CONFIG_LIST_GPT3 = autogen.config_list_from_json(
        env_or_file=json.dumps(
            [
                {"model": GPT35, "api_key": os.environ["OPENAI_API_KEY"]},
            ]
        )
    )

    CONFIG_LIST_GPT4 = autogen.config_list_from_json(
        env_or_file=json.dumps(
            [
                {"model": GPT4, "api_key": os.environ["OPENAI_API_KEY"]},
            ]
        )
    )
