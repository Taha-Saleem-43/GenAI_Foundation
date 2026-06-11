from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class StudyState(TypedDict):
    topic: str
    explanation: str
    questions: str
    answers: str
    feedback: str
    
def explain_topic(state: StudyState):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Explain this topic simply: {state['topic']}"
        }]
    )

    return {"explanation": res.choices[0].message.content}


def generate_questions(state: StudyState):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
Based on this explanation:
{state['explanation']}

Generate 3 short quiz questions.
"""
        }]
    )

    return {"questions": res.choices[0].message.content}


def student_answers(state: StudyState):
    answers = "Sample answers provided by student"
    return {"answers": answers}

# def student_answers(state: StudyState):
#     print("\n--- Quiz Questions ---\n")
#     print(state["questions"])

#     answers = input("\nEnter your answers here:\n")

#     return {"answers": answers}

def evaluate(state: StudyState):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
Questions:
{state['questions']}

Student Answers:
{state['answers']}

Give feedback and score out of 10.
"""
        }]
    )

    return {"feedback": res.choices[0].message.content}


graph = StateGraph(StudyState)

graph.add_node("explain", explain_topic)
graph.add_node("quiz", generate_questions)
graph.add_node("answer", student_answers)
graph.add_node("evaluate", evaluate)

graph.set_entry_point("explain")

graph.add_edge("explain", "quiz")
graph.add_edge("quiz", "answer")
graph.add_edge("answer", "evaluate")
graph.add_edge("evaluate", END)

app = graph.compile()

result = app.invoke({
    "topic": "Machine Learning"
})

print(result["feedback"])