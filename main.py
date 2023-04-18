from dotenv import load_dotenv

import converter
import learner
from questions import GenerateQuestion, CheckQuestion
from quiz import StartQuiz, Stats, Answer

if __name__ == "__main__":
    load_dotenv()
    converter.Checker()
    StartQuiz("chapter25")
    # Stats([Answer("test 1", "answer", 0.2), Answer("test 1", "answer", 0.23), Answer("test 1", "answer", 0.62)])
    # questions = (GenerateQuestion("chapter24", 3))
    # answer = input(questions[0]["question"])
    # print(CheckQuestion("chapter24", 3, questions[0]["question"], answer))
