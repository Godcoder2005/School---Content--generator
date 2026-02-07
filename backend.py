from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
import json
from typing import Dict
from typing import Literal, List

load_dotenv()

# State 
class MCQ(TypedDict):
    question:str
    options:Dict[Literal["A", "B", "C", "D"], str]
    answer: Literal["A", "B", "C", "D"]

class School_agent(TypedDict):
    topic:str
    grade:int
    explanation:str
    mcq_questions:List[MCQ]
    status:Literal['pass','fail']
    feedback:str

# All tyes of pydantic classes
class mcq(BaseModel):
    question:str = Field(...,description="question")
    options: Dict[Literal["A","B","C","D"], str] = Field(...,description="options")
    answer:Literal["A","B","C","D"] = Field(...,description="answer")

class generate_agent_output(BaseModel):
    explanation:str = Field(...,description="explanation according to grade level")
    mcq_questions:List[mcq] = Field(...,description="mcq questions according to grade level")

class review_agent_output(BaseModel):
    status:Literal['pass','fail'] = Field(...,description="status")
    feedback:List[str] = Field(...,description="feedback")
    
# Defining the llm
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)

# Defining the structured output for review agent
review_llm = llm.with_structured_output(review_agent_output)

# Defining the structured output for generate agent
generate_llm = llm.with_structured_output(generate_agent_output)

# Generating agent session
def generate_agent(state: School_agent) -> dict:
    prompt = f"""
You are an expert elementary school teacher and curriculum designer.

Your task is to generate HIGH-QUALITY educational content
for the given student grade and topic.

-----------------------------------
INPUT
-----------------------------------
Grade: {state['grade']}
Topic: {state['topic']}

-----------------------------------
CONTENT RULES
-----------------------------------
- Language MUST strictly match the student’s grade level.
- Explanation must be:
  • clear
  • simple
  • conceptually correct
  • engaging with easy examples
- Do NOT include concepts beyond the syllabus.
- Generate EXACTLY 3 multiple-choice questions (MCQs).
- Each MCQ must:
  • test understanding of the explanation
  • contain exactly four options labeled A, B, C, D
  • have ONLY ONE correct answer
- MCQs must be directly derived from the explanation.
- Avoid difficult vocabulary and ambiguity.

-----------------------------------
OUTPUT RULES (VERY STRICT)
-----------------------------------
- Return ONLY valid JSON.
- Do NOT include markdown, comments, or extra text.
- Structure must remain deterministic.

-----------------------------------
RETURN FORMAT
-----------------------------------
{{
  "explanation": "string",
  "mcq_questions": [
    {{
      "question": "string",
      "options": {{
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      }},
      "answer": "A | B | C | D"
    }}
  ]
}}
"""

    result : generate_agent_output = generate_llm.invoke(prompt)
    return {
        "explanation": result.explanation,
        "mcq_questions": [q.model_dump() for q in result.mcq_questions]
    }

# This section below tells us about the review_agent
def review_agent(state:School_agent)->dict:
    prompt = f"""
You are an expert school curriculum reviewer and child education specialist.

Your task is to STRICTLY evaluate AI-generated educational content.
You must NOT rewrite, improve, or regenerate the content.
You only analyze and return a structured judgment.

-----------------------------------
INPUT
-----------------------------------
You will receive JSON with:

- grade: {state['grade']} (integer)
- topic: {state['topic']} (string)
- explanation: {state['explanation']} (string)
- mcqs: {state['mcq_questions']} (list of questions with options A–D and one correct answer)

-----------------------------------
EVALUATION CRITERIA
-----------------------------------

1. Age Appropriateness
   - Vocabulary must match the given grade.
   - Sentences must not be too complex.
   - No concepts beyond the grade syllabus.

2. Conceptual Correctness
   - Explanation must be factually correct.
   - Each MCQ’s correct answer must truly be correct.
   - Questions must directly relate to the explanation.

3. Clarity
   - Explanation should be easy to understand.
   - MCQs must be unambiguous and clearly worded.

-----------------------------------
DECISION RULE
-----------------------------------

- If ANY issue is found → status = "fail"
- If content is fully correct and appropriate → status = "pass"
- Be strict and objective like an academic reviewer.

-----------------------------------
OUTPUT FORMAT (STRICT)
-----------------------------------

Return ONLY valid JSON:

{{
  "status": "pass" | "fail",
  "feedback": ["short clear issue 1", "short clear issue 2"]
}}

Rules:
- Do NOT include any text outside JSON.
- If status = "pass", feedback must be an empty list [].
- Feedback must be concise and specific.
"""

    res:review_agent_output = review_llm.invoke(prompt)
    return {
        "status": res.status,
        "feedback": res.feedback
    }


graph = StateGraph(School_agent)
graph.add_node("generator_agent",generate_agent)
graph.add_node('review_agent',review_agent)


graph.add_edge(START,'generator_agent')
graph.add_edge('generator_agent','review_agent')
graph.add_edge('review_agent',END)

workflow = graph.compile()

