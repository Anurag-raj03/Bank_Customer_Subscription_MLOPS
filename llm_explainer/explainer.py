import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_explainer.utils import format_customer_input

load_dotenv()

llm = ChatOpenAI(
    temperature=0.3,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

with open("llm_explainer/llm_prompt.txt", "r") as file:
    prompt_template = PromptTemplate(
        input_variables=["customer_data", "prediction"],
        template=file.read()
    )

chain = LLMChain(llm=llm, prompt=prompt_template)

def generate_explanation(user_input: dict, prediction: str) -> str:
    formatted_input = format_customer_input(user_input)
    response = chain.run(customer_data=formatted_input, prediction=prediction)
    return response.strip()
