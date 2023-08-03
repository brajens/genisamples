import streamlit as st
import boto3
import json
from typing import Dict
from langchain import PromptTemplate, SagemakerEndpoint, LLMChain
from langchain.llms.sagemaker_endpoint import LLMContentHandler

modelendpoint = "jumpstart-XXXXXXXXXX-text2text-flan-t5-xxl"
thenewline,bold, unbold = "\n", "\033[1m", "\033[0m"

## Create Content Handler for input and output 
## It would change per model. Current handler is for FLAN T5 models
class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
        input_str = json.dumps({'text_inputs': prompt, **model_kwargs})
        return input_str.encode('utf-8')
      
    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json["generated_texts"][0]

## Initiate Model
content_handler = ContentHandler()
llm = SagemakerEndpoint(
    endpoint_name = modelendpoint, 
    region_name = "eu-west-1", 
    model_kwargs={"temperature": 1, "max_length": 500},
    content_handler = content_handler
)

st.markdown("## Generic LLM Client")
st.info("(Using JumpStart, Bedrock)")

txtquery = st.text_area("Your query:", "")

if(st.button("Response")):
    query = txtquery.title()
    response = llm(query)
    st.markdown("#### Response:")
    st.write(response)
