# handles all the llm stuff - groq + langchain setup

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from config import GROQ_API_KEY, GROQ_MODEL, TEMPERATURE, MAX_TOKENS, SYSTEM_MSG

# initialize the llm
def init_llm():
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return llm

# build the chain
def build_chain(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_MSG),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])
    return prompt | llm | StrOutputParser()


# convert the streamlit session messages into langchain format
def convert_history(messages):
    result = []
    for m in messages:
        if m["role"] == "user":
            result.append(HumanMessage(content=m["content"]))
        else:
            result.append(AIMessage(content=m["content"]))
    return result

# stream the response token by token
def ask_stream(chain, question, history):   
    buffer = ""
    inside_think = False
 
    for chunk in chain.stream({"question": question, "history": history}):
        buffer += chunk
 
        if not inside_think and "<think>" in buffer:
            inside_think = True
            before = buffer.split("<think>")[0]
            if before:
                yield before
            buffer = "<think>" + buffer.split("<think>", 1)[1]
 
        if inside_think:
            if "</think>" in buffer:
                after = buffer.split("</think>", 1)[1]
                inside_think = False
                buffer = after
                if after:
                    yield after
        else:
            yield chunk
            buffer = ""