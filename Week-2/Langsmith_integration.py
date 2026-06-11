from langgraph.graph import StateGraph, END
from typing import TypedDict
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


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
            "content": f"Generate 3 quiz questions:\n{state['explanation']}"
        }]
    )
    return {"questions": res.choices[0].message.content}


def student_answers(state: StudyState):
    answers = "Sample answers provided by student"
    return {"answers": answers}


# def student_answers(state: StudyState):
#     print("\n--- QUIZ QUESTIONS ---\n")
#     print(state["questions"])

#     answers = input("\nEnter your answers:\n")
#     return {"answers": answers}


def evaluate(state: StudyState):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
Questions:
{state['questions']}

Answers:
{state['answers']}

Give score out of 10 and feedback.
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