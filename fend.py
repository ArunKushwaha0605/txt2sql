"""Streamlit UI for the Text-to-SQL Agent"""
import streamlit as st
import pandas as pd
# import re
from app import TextToSQLAgent

# ---------- Page Config ----------
st.set_page_config(
    page_title="Text-to-SQL Agent",
    page_icon="🗄️",
    layout="wide"
)

st.header("Start Querying your DB....")


if "agent" not in st.session_state:
    st.session_state.agent = None

# # ---------- Initialize Agent ----------
# @st.cache_resource
# def load_agent():
#     return TextToSQLAgent()

# try:
#     agent = load_agent()
#     connected = True
# except Exception as e:
#     st.error(f"❌ Database connection failed: {e}")
#     connected = False
#     st.stop()

# ---------- Initialize Chat History ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Sidebar ----------
with st.sidebar:

        # ---------- Custom Styling ----------
    st.markdown("""
    <style>
        .stApp { background-color: #fafafa; }
        .main-header {
            background: linear-gradient(60deg, #667eea 0%, #764ba2 100%);
            padding: 1.0rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
            position: fixed;
            top: 0;            
        }
        .sql-box {
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 1rem;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------- Header ----------
    st.markdown("""
    <div class="main-header">
        <h1>🗄️ SQLaa</h1>
        
    </div>
    """, unsafe_allow_html=True)


    # st.sidebar.markdown("### 🗄️ Database Type")

    # st.radio(
    #     "Select Database",
    #     [
    #         "MySQL",
    #         "PostgreSQL (Coming Soon)",
    #         "SQL Server (Coming Soon)",
    #         "SQLite (Coming Soon)"
    #     ],
    #     index=0,
    #     disabled=True
    # )

    with st.sidebar.expander("🗄️ Database Type (coming soon..)"):
         st.radio(
            "Select Database",
            [
                "MySQL",
                "PostgreSQL",
                "SQL Server",
                "SQLite"
            ],
            index=0,
            disabled=True
        ) 


    with st.expander("Connection"):
        
        host=st.text_input(
            "Host",
            value="localhost"
        )
        port = st.text_input(
            "Port",
            value="3306"
        )
        user = st.text_input(
            "User",
            value="root"
        )
        password = st.text_input(
            "Password",
            type="password"
        )
        database = st.text_input(
            "Database",
            value='world'
        )

        if st.button("Connect"):
            try:
                    st.session_state.agent = TextToSQLAgent(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database
                )
                    st.success("✅ Connected successfully!")
                    # st.rerun()
            except Exception as e:
                    st.error(f"❌ Connection failed: {e}")

    if st.session_state.agent:
        st.success("✅ Connected")
    else:
        st.warning("⚠️ Not Connected")

    # st.markdown("### 🔌 Connection Status")
    # st.success("✅ Connected to MySQL")

    with st.expander("📋 Available Tables"):
        if st.session_state.agent:
            for table in st.session_state.agent.get_table_names():
                st.markdown(f"- `{table}`")

    # with st.expander("📐 View Schema"):
    #     st.code(agent.get_schema_info(), language="sql")

    with st.expander("💡 Sample Questions"):
        samples = [
        "Fetch the independence year of Angola?",
        "What is the Life Expectancy in India?",
        "Fetch the language of Azerbaijan.",
        "Fetch the language of Azerbaijan using joins.",
        "Fetch the highest populated district of Argentina and with number of population?",

        ]
        for q in samples:
                if st.session_state.agent:
                    if st.button(
                        q, 
                        key=f"sample_{q}", use_container_width=True):
                            st.session_state.pending_question = q
                            st.rerun()

    
#     sample_question = st.selectbox(
#     "💡 Sample Questions",
#     [
#         "",
#         "How many students are enrolled in GenAI?",
#         "Which student got the highest placement package?",
#         "List all students from Bangalore",
#         "What is the average package by course?",
#         "Show total revenue from each course"
#     ]
# )

#     if sample_question:

#         st.session_state.pending_question = sample_question
#         st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


    
    with st.expander("About"):
        st.write(
            "<p style='text-align: center; color: #888;'>"
    "Built with LangGraph + Streamlit + MySQL"
    "</p>",
    unsafe_allow_html=True)

# ---------- Helper: parse raw result into DataFrame ----------
def try_parse_to_df(raw_result: str):
    """Attempt to parse the SQLDatabase.run() string output into a DataFrame."""
    try:
        # SQLDatabase.run returns a string like "[('Rahul', 24.5), ('Priya', 22.0)]"
        data = eval(raw_result)
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], tuple):
            return pd.DataFrame(data)
    except Exception:
        pass
    return None

# ---------- Display Chat History ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            st.markdown(msg["content"]["answer"])

            with st.expander("🔍 View SQL Query"):
                st.code(msg["content"]["sql_query"], language="sql")

            df = try_parse_to_df(msg["content"]["raw_result"])
            if df is not None and not df.empty:
                with st.markdown("📊 View Result Data"):
                    st.dataframe(df, use_container_width=True)
            else:
                with st.markdown("📄 Raw Result"):
                    st.text(msg["content"]["raw_result"])

# ---------- Handle Input ----------
question = None

# From sample button click
if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question

# From chat input
user_input = st.chat_input("Ask a question about your database...")
if user_input:
    question = user_input

# ---------- Process Question ----------

if st.session_state.agent is None:

    st.warning(
        "Please connect to a database first."
    )

    st.stop()

if question:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking... generating SQL and querying database..."):
            try:
                result = st.session_state.agent.query(question)

                st.markdown(result["answer"])

                with st.expander("🔍 View SQL Query"):
                    st.code(result["sql_query"], language="sql")

                df = try_parse_to_df(result["raw_result"])
                if df is not None and not df.empty:
                    with st.markdown("📊 View Result Data"):
                        st.dataframe(df, use_container_width=True)
                else:
                    with st.markdown("📄 Raw Result"):
                        st.text(result["raw_result"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result
                })
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": {"answer": error_msg, "sql_query": "", "raw_result": ""}
                })


