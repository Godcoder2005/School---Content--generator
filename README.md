# 📚 AI Educational Content Generator & Reviewer

An **agent-based AI prototype** that automatically generates **grade-appropriate educational content** and then **reviews its own output** for correctness, clarity, and age suitability.

This project was developed as part of a **company assignment** to demonstrate:

* Structured LLM outputs
* Multi-agent reasoning
* Automated quality evaluation
* Simple interactive UI

---

# 🧠 Project Overview

The system consists of **two AI agents**:

### 1️⃣ Generator Agent

* Takes **grade** and **topic** as input
* Produces:

  * Simple explanation
  * 3 MCQ questions with correct answers
* Ensures:

  * Age-appropriate language
  * Conceptual correctness
  * Deterministic JSON structure

---

### 2️⃣ Reviewer Agent

* Evaluates the generated content based on:

  * **Age appropriateness**
  * **Concept correctness**
  * **Clarity**
* Returns:

  * `pass` or `fail`
  * Structured feedback list
* Enables **automatic refinement** if issues are found.

---

# 🔁 Agent Workflow

```
User Input → Generator Agent → Reviewer Agent
                         ↓
                (If fail → regenerate once)
                         ↓
                     Final Output
```

This demonstrates a **real AI agent pipeline** rather than a simple prompt-response system.

---

# 🖥️ Streamlit UI Features

* Enter **grade** and **topic**
* View:

  * Generated explanation
  * MCQs with answers
  * Review status
  * Reviewer feedback
* Clean, minimal interface for **prototype demonstration**

---

# 🛠️ Tech Stack

* **Python**
* **LangGraph** – agent workflow orchestration
* **LangChain** – LLM integration
* **Google Gemini API** – content generation & review
* **Pydantic** – structured output validation
* **Streamlit** – interactive UI

---

# 📂 Project Structure

```
project/
│
├── backend.py        # LangGraph agents + workflow
├── frontend.py       # Streamlit UI
├── requirements.txt  # Dependencies
├── .env              # API keys (not committed)
└── README.md
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone the repository

```bash
git clone <repo-link>
cd project
```

## 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Add environment variables

Create `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

---

# ▶️ Run the Application

```bash
streamlit run frontend.py
```

The app will open in your browser.

---

# 🌍 Deployment

The project can be deployed easily using:

* **Streamlit Community Cloud** (recommended for prototype)
* Render / Railway (for backend deployment)

---

# 🎯 Key Learning Outcomes

* Designing **multi-agent AI systems**
* Enforcing **structured JSON outputs**
* Implementing **automated quality review**
* Building **LLM-powered educational tools**
* Deploying **interactive AI applications**

---

# 📌 Future Improvements

* FastAPI production backend
* Database for content history
* Multi-topic curriculum generation
* Teacher dashboard & analytics
* Support for multiple languages

---

# 👨‍💻 Author

**Akshith Kumar**
B.Tech Student | AI & GenAI Enthusiast

* Strong interest in **AI agents, LLM systems, and real-world deployment**
* Passionate about building **practical AI tools**, not just demos.

---

# ⭐ Submission Note

This repository demonstrates a **complete working prototype** fulfilling the assignment requirements:

* Dual-agent architecture
* Structured outputs
* Review & refinement logic
* Interactive UI

Designed to reflect **real-world AI engineering practices** at a prototype scale.

---
