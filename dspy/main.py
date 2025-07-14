import dspy
import os

from secret import *
from litellm import completion
from dspy.datasets import HotPotQA

def init_lm():
    os.environ["AZURE_API_KEY"] = api_key
    os.environ["AZURE_API_BASE"] = api_base
    os.environ["AZURE_API_VERSION"] = api_version
    lm = dspy.LM(model_name)
    dspy.configure(lm=lm)
    lm("Say this is a test!", temperature=0.7)  # => ['This is a test!']
    resp = lm(messages=[{"role": "user", "content": "Say this is a test!"}])  # => ['This is a test!']
    print(resp)


def math_demo():
    init_lm()
    math = dspy.ChainOfThought("question -> answer: float")
    resp = math(question="Two dice are tossed. What is the probability that the sum equals two?")
    print(resp)


class Classify(dspy.Signature):
    """Classify sentiment of a given sentence."""
    from typing import Literal
    sentence: str = dspy.InputField()
    sentiment: Literal['positive', 'negative', 'neutral'] = dspy.OutputField()
    confidence: float = dspy.OutputField()

def classification_demo():
    init_lm()
    classify = dspy.Predict(Classify)
    resp = classify(sentence="This book was super fun to read, though not the last chapter.")
    print(resp)


def litellm():
    # azure call
    response = completion(
        model=model_name,
        messages=[{"content": "Hello, how are you?", "role": "user"}]
    )
    print(response)

def search_wikipedia(query: str) -> list[str]:
    results = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
    return [x['text'] for x in results]


def search_wikipedia_demo():
    rag = dspy.ChainOfThought('context, question -> response')
    question = "What's the name of the castle that David Gregory inherited?"
    resp = rag(context=search_wikipedia(question), question=question)
    print(resp)


def react_demo():
    react = dspy.ReAct("question -> answer", tools=[search_wikipedia])
    tp = dspy.MIPROv2(metric=dspy.evaluate.answer_exact_match, auto="light", num_threads=24)
    optimized_react = tp.compile(react, trainset=trainset)
    print(optimized_react)

class RAG(dspy.Module):
    def __init__(self, num_docs=5):
        self.num_docs = num_docs
        self.respond = dspy.ChainOfThought('context, question -> response')

    def forward(self, question):
        context = search(question, k=self.num_docs)   # defined in tutorial linked below
        return self.respond(context=context, question=question)

def rag_demo():
    tp = dspy.MIPROv2(metric=dspy.evaluate.SemanticF1(decompositional=True), auto="medium", num_threads=24)
    optimized_rag = tp.compile(RAG(), trainset=trainset, max_bootstrapped_demos=2, max_labeled_demos=2)

if __name__ == '__main__':
    init_lm()
    # classification_demo()





