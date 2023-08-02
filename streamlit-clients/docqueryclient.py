import streamlit as st
import boto3
import json

kendraindex = '<Kendra Index ID>'
modelendpoint = "jumpstart-XXXXXX-text2text-flan-t5-xxl"
thenewline,bold, unbold = "\n", "\033[1m", "\033[0m"

def query_endpoint(encoded_text, endpoint_name):
    client = boto3.client("runtime.sagemaker")
    response = client.invoke_endpoint(
        EndpointName=endpoint_name, ContentType="application/x-text", Body=encoded_text
    )
    return response

def parse_response(query_response):
    model_predictions = json.loads(query_response["Body"].read())
    generated_text = model_predictions["generated_text"]
    return generated_text

st.markdown("## Enterprise Search")
st.info("(Using Amazon Kendra, JumpStart, Bedrock)")

txtquery = st.text_input("Your query:", "")

if(st.button("Query")):
    query = txtquery.title()
    kclient = boto3.client('kendra')
    response = kclient.retrieve(IndexId=kendraindex, QueryText=query)
    context = response["ResultItems"][0]["Content"]
    prompt = "Answer based on context:" + thenewline + context + thenewline + query
    query_response = query_endpoint(prompt.encode("utf-8"), endpoint_name=modelendpoint)
    model_predictions = json.loads(query_response["Body"].read())
    st.markdown("#### Response:")
    st.write(model_predictions["generated_text"])
