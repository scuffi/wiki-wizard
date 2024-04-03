import requests
import streamlit as st

from database import redis_client

def generate_page(title: str, notion_url: str, notion_api_key: str, openai_api_key: str):
    body = {
        "title": title,
    }
    
    headers = {
        "page-url": notion_url,
        "notion-secret": notion_api_key,
        "oai-key": openai_api_key,
    }
    
    response = requests.post("http://engine:8000/generate", json=body, headers=headers)
    
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(f"Could not add **{title}** to generation queue. {response.text}")

st.markdown("# 🪄 WikiWizard")

st.markdown("Enter a topic to generate a wiki for.")

with st.expander("Configuration"):
    config_col1, config_col2 = st.columns([3,1])

    with config_col1:
        notion_url = st.text_input("Notion URL", key="notion_url", value=redis_client.get("config.notion_url"))
        notion_api_key = st.text_input("Notion API Key", key="notion_api_key", type="password", value=redis_client.get("config.notion_api_key"))
        openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password", value=redis_client.get("config.openai_api_key"))

    with config_col2:
        st.button("Update", key="notion_url_update_button", on_click=redis_client.set, args=("config.notion_url", st.session_state.notion_url))
        st.button("Update", key="notion_api_key_update_button", on_click=redis_client.set, args=("config.notion_api_key", st.session_state.notion_api_key))
        st.button("Update", key="openai_api_key_update_button", on_click=redis_client.set, args=("config.openai_api_key", st.session_state.openai_api_key))

col1, col2 = st.columns([3,1])
with col1:
    topic = st.text_input("Topic", key="topic_input")

with col2:
    generate = st.button("Generate", key="generate_button", on_click=generate_page, args=(topic, notion_url, notion_api_key, openai_api_key))
    
with st.container(border=True):
    st.markdown("## Generations")
    
    for key in redis_client.keys(pattern="generation:*"):
        with st.container(border=True):
            st.markdown(f"**{redis_client.hget(key, 'title')}**")
            st.markdown(redis_client.hget(key, "status"))
            st.button("🗑️", on_click=redis_client.delete, args=(key,))
