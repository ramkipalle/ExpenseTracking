from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os


load_dotenv()

print(os.getenv("OPENAI_API_KEY"))


class Calendar_Specs(BaseModel):
    transaction_date: str = Field(description="Transaction date in YYYY-MM-DD format")
    merchant_name: str = Field(description="The name of the merchant")
    amount: float = Field(description="The amount of the transaction")
    last_four_digits: str = Field(description="The last 4 digits of the card")


# Setup a parser for the output
output_parser = JsonOutputParser(pydantic_object=Calendar_Specs)

# Setup the prompt
template = """You are a helpful assistant who generates the details for a
 credit card transaction details in JSON format only.
 A user will pass in a request and you will convert it into a JSON
 structure extracting the transaction date in YYYY-MM-DD format, 
 merchant name, amount and last four digits of the card. 
 ONLY return JSON and nothing else."""

human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

# Setup the chain
model = ChatOpenAI()
chain = chat_prompt | model | output_parser
