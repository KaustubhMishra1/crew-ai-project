from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os
import litellm

load_dotenv()

# Temporary patch: Groq abhi 'cache_breakpoint' field support nahi karta,
# jo CrewAI internally add karta hai. Isko strip karke bhejte hain.
_original_completion = litellm.completion

def _patched_completion(*args, **kwargs):
    if "messages" in kwargs:
        for msg in kwargs["messages"]:
            if isinstance(msg, dict):
                msg.pop("cache_breakpoint", None)
    return _original_completion(*args, **kwargs)

litellm.completion = _patched_completion
llm = LLM(
    model= "groq/openai/gpt-oss-20b",
    api_key=os.getenv("Grok_api_key")
)
researcher = Agent(
    role="Senior Research Analyst",
    goal="Find accurate and up-to-date information on a given topic",
    backstory="You are an experienced research analyst known for thorough, fact-based research.",
    tools=[search_tool],
    llm=llm
)
research_task = Task(
    description="Research the topic 'benefits of renewable energy' and summarize the top 3 key points with brief supporting facts.",
    expected_output="A bullet-point summary with exactly 3 key points, each with a short explanation.",
    agent=researcher
)

writer = Agent(
    role="Content Writer",
    goal="Write clear, engaging summaries based on research findings",
    backstory="You are a skilled writer who transforms raw research into polished, easy-to-read content.",
    llm=llm
)
writing_task = Task(
    description="Using the research provided, write a short, engaging paragraph (4-5 sentences) summarizing the benefits of renewable energy for a general audience.",
    expected_output="A well-written paragraph, 4-5 sentences, in simple non-technical language.",
    agent=writer,
    context=[research_task]
)
reviewer = Agent(
    role="Quality Reviewer",
    goal="Ensure content is accurate, engaging, and free of errors before final delivery",
    backstory="You are a meticulous editor who checks facts, tone, and clarity, and suggests improvements when needed.",
    llm=llm
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
print(result)