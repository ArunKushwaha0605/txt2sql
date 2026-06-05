"""
Text-to-SQL Agent Backend using LangGraph + MySQL
"""
import os
from typing import TypedDict
from dotenv import load_dotenv

from langchain_community.utilities import SQLDatabase

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

load_dotenv()


# ---------- State Definition ----------
class AgentState(TypedDict):
    question: str
    schema: str
    sql_query: str
    query_result: str
    final_answer: str
    error: str


# ---------- Agent Class ----------
class TextToSQLAgent:
    def __init__(
        self,
        host,
        port,
        user,
        password,
        database
    ):
        self.db = self._connect_db(
            host,
            port,
            user,
            password,
            database
        )
        # self.llm = ChatGoogleGenerativeAI(
        #     model="gemini-2.5-flash-lite", google_api_key=os.getenv("GOOGLE_API_KEY"),
        #     max_tokens=500, 
        #     temperature=0.0, 
        #     verbose=False)
        self.llm=ChatGroq(
            model= "qwen/qwen3-32b",
            temperature=0.0,
            reasoning_format="hidden",
            max_tokens=600,
            verbose=False
            )
        self.app = self._build_graph()

    def _connect_db(
        self,
        host,
        port,
        user,
        password,
        database
    ):
        uri = (
            f"mysql+pymysql://{user}:"
            f"{password}@"
            f"{host}:"
            f"{port}/"
            f"{database}"
        )
        return SQLDatabase.from_uri(uri)

    def get_table_names(self):
        return self.db.get_usable_table_names()

    def get_schema_info(self):
        return self.db.get_table_info()

    # ---------- Graph Nodes ----------
    def _get_schema(self, state: AgentState):
        return {"schema": self.db.get_table_info()}

    def _generate_sql(self, state: AgentState):
        prompt = ChatPromptTemplate.from_template("""
You are a MySQL expert. Based on the schema below, write a syntactically correct MySQL query to answer the user's question.

Schema:
{schema}

Question: {question}

Rules:
- Return ONLY the SQL query, no explanations, no markdown formatting, no backticks
- Use proper JOINs when needed
- Use LIMIT 10 unless the user specifies otherwise
- Never use DROP, DELETE, UPDATE, TRUNCATE, ALTER, INSERT

SQL Query:""")
        chain = prompt | self.llm
        response = chain.invoke({
            "schema": state["schema"],
            "question": state["question"]
        })
        sql = response.content.strip().replace("```sql", "").replace("```", "").strip()
        return {"sql_query": sql}

    def _validate_sql(self, state: AgentState):
        """Block destructive queries."""
        blocked = ["DROP", "DELETE", "UPDATE", "TRUNCATE", "ALTER", "INSERT"]
        query_upper = state["sql_query"].upper()
        for keyword in blocked:
            if keyword in query_upper:
                return {"error": f"Blocked: query contains '{keyword}'. Read-only mode."}
        return {"error": ""}

    def _execute_sql(self, state: AgentState):
        if state.get("error"):
            return {"query_result": state["error"]}
        try:
            result = self.db.run(state["sql_query"])
            return {"query_result": str(result) if result else "No results found."}
        except Exception as e:
            return {"query_result": f"Error executing query: {str(e)}"}

    def _generate_answer(self, state: AgentState):
        if state.get("error"):
            return {"final_answer": state["error"]}

        prompt = ChatPromptTemplate.from_template("""
Given the user's question, the SQL query, and the result, provide a clear, concise natural language answer.

Question: {question}
SQL Query: {sql_query}
Result: {query_result}

Provide a friendly, direct answer. If the result is empty, say so politely.

Answer:""")
        chain = prompt | self.llm
        response = chain.invoke({
            "question": state["question"],
            "sql_query": state["sql_query"],
            "query_result": state["query_result"]
        })
        return {"final_answer": response.content}

    # ---------- Build the LangGraph ----------
    def _build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("get_schema", self._get_schema)
        workflow.add_node("generate_sql", self._generate_sql)
        workflow.add_node("validate_sql", self._validate_sql)
        workflow.add_node("execute_sql", self._execute_sql)
        workflow.add_node("generate_answer", self._generate_answer)

        workflow.add_edge(START, "get_schema")
        workflow.add_edge("get_schema", "generate_sql")
        workflow.add_edge("generate_sql", "validate_sql")
        workflow.add_edge("validate_sql", "execute_sql")
        workflow.add_edge("execute_sql", "generate_answer")
        workflow.add_edge("generate_answer", END)

        return workflow.compile()

    # ---------- Public method ----------
    def query(self, question: str) -> dict:
        result = self.app.invoke({"question": question})
        return {
            "question": question,
            "sql_query": result.get("sql_query", ""),
            "raw_result": result.get("query_result", ""),
            "answer": result.get("final_answer", "")
        }

# # Quick standalone test
# if __name__ == "__main__":
#     agent = TextToSQLAgent()
#     print("Tables:", agent.get_table_names())
#     result = agent.query("Who is the instructor of Machine Learning course?")
#     print(result)