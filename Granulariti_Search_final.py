#!/usr/bin/env python
# coding: utf-8




import streamlit as st
from openai import OpenAI
import os
import time
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from getpass import getpass


# In[7]:


os.environ["SERPER_API_KEY"] = "SerperAPIKey"



# Sidebar for OpenAI API Key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
    if st.button("Start a new conversation"):
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
        ]
        st.experimental_rerun()
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# Title of the application
st.title("📚 Granulariti.ai Search")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Search the web for detailed and comprehensive."}
    ]

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
if prompt := st.chat_input(placeholder = "Please enter a query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
            
        llm = ChatOpenAI(model_name = "gpt-4o-mini", openai_api_key=openai_api_key)
        search = GoogleSerperAPIWrapper()
        
        try:
            search_response = search.run(prompt)
            summarize_prompt = (
                "Summarize the following search results into 3-5 sentences for readability:\n\n"
                f"{search_response}"
            )
            
            summary = llm.predict(summarize_prompt)
            
            with st.chat_message("assistant"):
                st.markdown("### **Search Result Summary**")
                st.write(summary)
                
        except Exception as e:
            st.error(f"Error: {e}")


# In[ ]:




