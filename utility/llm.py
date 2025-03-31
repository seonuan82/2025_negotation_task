from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

def get_llm_response(prompt, model="gpt-3.5-turbo", temperature=0.7):
    llm = ChatOpenAI(model_name=model, temperature=temperature)
    return llm([HumanMessage(content=prompt)]).content