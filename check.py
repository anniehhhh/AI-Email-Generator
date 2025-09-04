from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(
    temperature=0.3,
    groq_api_key="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",
    model_name="llama3-70b-8192"
)

response = llm.invoke("Say hello in a friendly tone")
print(response)


print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
