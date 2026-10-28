from services.gemini_service import get_ai_response
import time
time.sleep(2)
QUESTIONS = [
    "What is AI?",
    "Explain machine learning.",
    "What is Python?",
    "Give me a short explanation of APIs.",
    "Explain recursion to a beginner.",
]

for question in QUESTIONS:
    print("-" * 50)
    print(f"Q: {question}")

    try:
        answer = get_ai_response(question)
        print(f"A: {answer}")
    except Exception as e:
        print(f"[FAILED] {type(e).__name__}: {e}")