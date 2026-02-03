from dotenv import load_dotenv
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)

csv_file = "/workspaces/analise-agente/sales.csv"

df = pd.read_csv(csv_file,
                delimiter=";",
                low_memory=False
                )
df.columns = [
    "product_id", "local", "date", "planned_quantity", 
    "actual_quantity", "planned_price", "promotion_type", 
    "actual_price", "service_level"
]
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
df["promotion_type"] = df["promotion_type"].fillna("No Promotion")

df['quantity_difference'] = df['actual_quantity'] - df['planned_quantity']
df['price_difference'] = df['actual_price'] - df['planned_price']

python_tool = PythonAstREPLTool(
                locals={"df": df, "pd": pd},
                name="python_repl",
                description="""Ferramenta que utiliza python para análise de dados armazenados no dataframe 'df'. 
                            Você pode usar a biblioteca pandas (importada como 'pd') para manipular e analisar os dados. 
                            Use esta ferramenta apenas se o usuário pedir para analisar os dados de vendas.

                            Colunas do dataframe 'df':
                            - product_id: Identificador do produto.
                            - local: Local de venda.
                            - date: Data da venda.
                            - planned_quantity: Quantidade planejada para venda.
                            - actual_quantity: Quantidade realmente vendida.
                            - planned_price: Preço planejado para venda.
                            - promotion_type: Tipo de promoção aplicada.
                            - actual_price: Preço real de venda.
                            - service_level: Nível de serviço alcançado.
                            - quantity_difference: Diferença entre quantidade real e planejada.
                            - price_difference: Diferença entre preço real e planejado.

                            Retorne sempre o resultado final da análise."""
                )


llm = ChatGoogleGenerativeAI(
            model="gemini-3-pro-preview",
            temperature=0,
            max_tokens=1000,
            max_retries=2,
        )


system_prompt = """Você é um assistente de análise de dados.
                Use o dataframe 'df' para responder às perguntas do usuário sobre os dados de vendas.
                Você tem acesso à ferramenta de execução de código Python 'python_tool' para manipular e analisar o dataframe.
                Seja claro e objetivo em suas respostas."""

agent = create_agent(
    llm,
    [python_tool],
    system_prompt=system_prompt,
    )


decide = "y"
while decide in ["y", "yes", "sim", "s"]:
    user_message = input("Faça uma pergunta sobre os dados: ")
    output = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    print(output["messages"][-1].text)
    decide = input("Quer continuar essa conversa? y/n ").strip().lower()

print("Encerrando a conversa. Até mais!")
