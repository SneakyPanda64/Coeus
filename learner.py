import json

import gpt
from questions import GetContext


def GetExplanation(id, index):
    header, body = GetContext(id, index)
    context = (header + "\n\n" + body).strip()
    explanation = gpt.ChatCompletion([
        {"role": "system", "content": "You are an AI used for teaching business to students"},
        {"role": "user",
         "content": f"Write an explanation on the following topic while prioritising making it easy to understand and detailed. The following topic is relating to the UK.\n\ntopic:\n\n{context}"}
    ], 400, 0)
    return explanation