import streamlit as st
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os
import litellm
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()
load_dotenv()

_original_completion = litellm.completion

def _patched_completion(*args, **kwargs):
    if "messages" in kwargs:
        for msg in kwargs["messages"]:
            if isinstance(msg, dict):
                msg.pop("cache_breakpoint", None)
    return _original_completion(*args, **kwargs)

litellm.completion = _patched_completion
st.set_page_config(page_title="AI Crew", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a0e14 0%, #131b2e 50%, #0a0e14 100%);
        color: #e0e0e0;
    }
    
    h1 {
    font-family: 'Courier New', monospace;
    color: #00ff9d;
    text-align: center;
}
    
    .stButton button {
    background-color: #2a2f3e;
    color: #e0e0e0;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    padding: 0;
    transition: all 0.2s ease;
}
input[data-testid="stTextInputField"] {
    background-color: #1a1f2e !important;
    color: #e0e0e0 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 20px 16px !important;
    font-size: 16px !important;
}

input[data-testid="stTextInputField"]:focus {
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: none !important;
    outline: none !important;
}
.stButton button:hover {
    background-color: #3a3f4e;
}
.block-container {
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding-left: 2rem;
    padding-right: 2rem;
}
    </style>
""", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Research Agent</h2>", unsafe_allow_html=True)

st.markdown("""
    <p style='
        text-align: center; 
        font-weight: 300; 
        letter-spacing: 2px;
        color: "Black";
        text-transform: uppercase;
        margin-top: -10px;
    '>
       What you would like to know?
    </p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    input_col, button_col = st.columns([6, 1])
    with input_col:
        topic = st.text_input("", placeholder="Ask here...", label_visibility="collapsed")
    with button_col:
        submit = st.button("→", use_container_width=True)


if submit and topic:
    with st.chat_message("user"):
        st.write(topic)
    with st.chat_message("assistant"):
        with st.spinner("🔍 Researching..."):
            
        
            llm = LLM(
                model="groq/openai/gpt-oss-20b",
                api_key=os.getenv("Grok_api_key")
            )

            researcher = Agent(
                role="Senior Research Analyst",
                goal="Find accurate and up-to-date information on a given topic",
                backstory="You are an experienced research analyst known for thorough, fact-based research.",
                tools=[search_tool],
                llm=llm
            )

            writer = Agent(
                role="Content Writer",
                goal="Write clear, engaging summaries based on research findings",
                backstory="You are a skilled writer who transforms raw research into polished, easy-to-read content.",
                llm=llm
            )

            reviewer = Agent(
                role="Quality Reviewer",
                goal="Ensure content is accurate, engaging, and free of errors before final delivery",
                backstory="You are a meticulous editor who checks facts, tone, and clarity, and suggests improvements when needed.",
                llm=llm
            )

            research_task = Task(
                description=f"Research the topic '{topic}' and summarize the top 3 key points with brief supporting facts.",
                expected_output="A bullet-point summary with exactly 3 key points, each with a short explanation.",
                agent=researcher
            )

            writing_task = Task(
                description="Using the research provided, write a short, engaging paragraph (4-5 sentences) summarizing the topic for a general audience.",
                expected_output="A well-written paragraph, 4-5 sentences, in simple non-technical language.",
                agent=writer,
                context=[research_task]
            )

            review_task = Task(
                description="Review the written paragraph for factual consistency with the research, clarity, and tone. If it looks good, return it as-is with a brief note on why it works well. If there are issues, point them out and provide an improved version.",
                expected_output="The final approved paragraph, along with a short reviewer's note (1-2 sentences) on its quality.",
                agent=reviewer,
                context=[research_task, writing_task]
            )

            crew = Crew(
                agents=[researcher, writer, reviewer],
                tasks=[research_task, writing_task, review_task],
                verbose=True
            )

            result = crew.kickoff()

        st.success("Done!")
        st.markdown(result.raw)
    