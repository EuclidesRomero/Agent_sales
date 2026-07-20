from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY")
).bind_tools(tools)