import streamlit as st
import boto3
import json

smendpoint= "jumpstart-XXXXXXX-textgeneration-llama-2-7b"
thenewline,bold, unbold = "\n", "\033[1m", "\033[0m"

runtime= boto3.client('runtime.sagemaker')

sqlinstruction = "Create SQL statement from instruction."
sqlquery = "SQL statement:"
f = open("sqlexamples.txt","r")
sqlexamples = f.read()
f.close()

pythoninstruction = "Question: "
pythonquery = "Answer:"
f = open("pythonexamples.txt","r")
pythonexamples = f.read()
f.close()

st.markdown("## Generate Python Code and SQL Statements Based on Instructions")
st.info("(Using LLAMA-2, Bedrock)")

mode = st.radio("Select mode: ", ('Python Code', 'SQL'))
txtquery = st.text_area("Your query:", "")

if(st.button("Generate")):
    if (mode == 'SQL'):
        prompt = sqlexamples + thenewline + sqlinstruction + thenewline + txtquery.title() + thenewline + sqlquery
    else:
        prompt = pythonexamples + thenewline + pythoninstruction + txtquery.title() + thenewline + pythonquery
    
    payload = {
       "inputs": prompt,
       "parameters":{"max_new_tokens": 100, "top_p": 0.9, "temperature": 0.1, "return_full_text": False}
    }
    response = runtime.invoke_endpoint(EndpointName=smendpoint,
                                       ContentType='application/json',
                                       Body=json.dumps(payload),CustomAttributes="accept_eula=true")
    result = json.loads(response['Body'].read().decode())
    script = result[0]["generation"] 
    st.markdown("#### Response:")
    if (mode == 'SQL'):
        script = script[0:script.index(';')]
        st.code(script, language="sql", line_numbers=False)
    else:
        script = script[0:script.index('return result')+13]
        st.code(script, language="python", line_numbers=False)
    
