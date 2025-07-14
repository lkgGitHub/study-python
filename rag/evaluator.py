from llama_index.core.evaluation import CorrectnessEvaluator
from llama_index.llms.azure_openai import AzureOpenAI
from secret import *

llm_eva = AzureOpenAI(
    model=eva_model,
    engine=eva_engine,
    api_key=eva_api_key,
    azure_endpoint=eva_azure_endpoint,
    api_version=eva_api_version,
)
evaluator = CorrectnessEvaluator(llm=llm_eva)

query_reference_reference = [

]

for query, reference ,response in query_reference_reference:
    result = evaluator.evaluate(
        query=query,
        response=response,
        reference=reference,
    )
    print("query:", query, result.score)
