import textwrap

import learner
import questions
from statistics import mean, mode
class Answer:
    def __init__(self, question, answer, correctness):
        self.question = question
        self.answer = answer
        self.correctness = correctness
    def __str__(self):
        return f"Answer(question: {self.question}, answer: {self.answer}, correctness: {self.correctness})"
def StartQuiz(id):
    headers, _ = questions.ReadDocument(id)
    print("Content:")
    for i, v in enumerate(headers):
        print(f"- [{i+1}] {v}")
    selection = int(input(f"Which sub-topic would you like to revise? [1-{len(headers)}]: "))
    SubTopic(id, selection - 1)

def SubTopic(id, index):
    explanation = learner.GetExplanation(id, index)
    wrapper = textwrap.TextWrapper(width=100)

    print("=" * 20)
    for v in explanation.split("\n\n"):
        word_list = wrapper.wrap(text=v)
        for v in word_list:
            print(v)
        print("\n")
    print("=" * 20)
    SubTopicQuestions(id, index)
def SubTopicQuestions(id, index,):
    qs = questions.GenerateQuestion(id, index)
    answers = []
    for i, question in enumerate(qs):
        print("=" * 20)
        print(f"Question ({i + 1}/{len(qs)})", question["question"] + "\n\n")
        answer = input("Answer: ")
        if answer != "skip":
            response = questions.CheckQuestion(id, index, question["question"], answer)
            print(f"Correctness:", str(response["correctness"] * 100) + "%")
            if response["correctness"] < 0.9:
                print(f"Comments:", "\n".join(response["comments"]))
                print(f"Model Answer:", response["model_answer"])
            answers.append(Answer(question, answer, response["correctness"]))
    if len(answers) > 0:
        Stats(answers)
    try_again = input("Would you like to try again? [y/N]: ")
    if try_again.upper() == "Y":
        SubTopicQuestions(id, index)

def Stats(answers):
    correctness = [float(i.correctness) for i in answers]
    print(correctness)
    print("="*20)
    print("Statistics:")
    print(f"- Questions: {len(answers)}")
    print(f"  -> Correct: {len([i for i in answers if i.correctness >= 0.9])}")
    print(f"  -> Incorrect: {len([i for i in answers if i.correctness < 0.9])}")
    print(f"- Correctness")
    print(f"  -> Mean: {mean([float(i.correctness) for i in answers])* 100}%")
    print(f"  -> Mode: {mode([float(i.correctness) for i in answers]) * 100}%")
    print(f"  -> Range: {sorted(correctness)[0]* 100}% - {sorted(correctness)[-1] * 100}%")
    print("=" * 20)
# def GenerateQuiz(id, index):
#     explanation = learner.GetExplanation(id, index)
#     qs = questions.GenerateQuestion(id, index)
#     return explanation, qs