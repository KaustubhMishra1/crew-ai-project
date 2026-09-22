# crew-ai-project
# 🤖 AI Crew – Multi-Agent Research Assistant

## 📌 Overview

AI Crew is a multi-agent research assistant built using **CrewAI and Streamlit**. It simulates a collaborative workflow where multiple AI agents work together to research, write, and review content on any given topic.

The system integrates **real-time web search using Serper API**, allowing agents to fetch up-to-date information before generating responses.

---

## 🚀 Key Features

* Multi-agent workflow (Researcher → Writer → Reviewer)
* 🔍 Real-time web search using **SerperDevTool (Google Search API)**
* Structured and concise output generation
* Automated content quality checking
* Clean and interactive Streamlit UI
* LLM-powered reasoning and summarization

---

## 🧠 How It Works

1. User enters a topic in the UI
2. **Research Agent** uses Serper API to fetch real-time data
3. **Writer Agent** converts research into a readable summary
4. **Reviewer Agent** validates accuracy and improves clarity
5. Final refined output is displayed

---

## 🛠️ Tech Stack

* Python
* Streamlit
* CrewAI
* LiteLLM
* Groq LLM API
* **Serper API (via SerperDevTool)**
* dotenv

---

## 📂 Project Structure

```id="e9g2t3"
project/
│── app.py  
│── .env  
│── requirements.txt  
│── README.md  
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash id="n1k9s0"
git clone https://github.com/your-username/ai-crew.git
cd ai-crew
```

### 2️⃣ Install dependencies

```bash id="2j8dka"
pip install -r requirements.txt
```

### 3️⃣ Setup environment variables

Create a `.env` file and add:

```id="j82nqk"
Grok_api_key=your_api_key_here
SERPER_API_KEY=your_serper_key_here
```

### 4️⃣ Run the app

```bash id="f8d9sl"
streamlit run app.py
```

---

## 💡 Example Use Case

Ask:

> "Latest trends in AI agents"

✔ System will:

* Fetch **real-time data using Serper (Google search)**
* Summarize key insights
* Validate and refine output

---

## ⚠️ Limitations

* Depends on external APIs (Groq, Serper)
* Response quality depends on search results + LLM
* Not deployed yet (runs locally)

---

## 🔮 Future Improvements

* Add memory (conversation context)
* Improve UI/UX
* Streaming responses
* Deployment on Streamlit Cloud
* Multi-source search integration

---

## 👨‍💻 Author

**Kaustubh Mishra**

---

## ⭐ Why This Project Matters

This project demonstrates:

* Multi-agent AI system design
* Integration of **LLMs with external tools (Serper API)**
* Real-time data fetching + reasoning
* End-to-end AI application development

---
