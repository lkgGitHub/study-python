import os
from llama_index.core.evaluation import CorrectnessEvaluator
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
from llama_index.embeddings.siliconflow import SiliconFlowEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.llms.azure_openai import AzureOpenAI
from secret import *

# pip install llama-index-llms-azure-openai
# pip install docx2txt 
# pip install openpyxl
# ppt: nlpconnect/vit-gpt2-image-captioning

embed_model = SiliconFlowEmbedding(
    model=embedding_model,
    api_key=embedding_model_api_key,
)

os.environ["OPENAI_API_KEY"] = "xxx"

llm = OpenAILike(
    model=llm_model,
    api_base=llm_api_base,
    api_key=llm_api_key,
    is_chat_model=True,
    is_function_calling_model=True,
    max_tokens=1024,  
    temperature=0.1,
    top_p=0.3,
)

from llama_index.core import Settings
Settings.embed_model = embed_model
Settings.llm = llm


file_dir = ""
documents = SimpleDirectoryReader(file_dir).load_data()


from llama_index.core.node_parser import SentenceSplitter

# 固定大小分块:
text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)

# 语义分块
# from llama_index.core.node_parser import SemanticSplitterNodeParser
# text_splitter = SemanticSplitterNodeParser(
#     buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
# )


# global
from llama_index.core import Settings

Settings.text_splitter = text_splitter

# per-index
index = VectorStoreIndex.from_documents(
    documents, transformations=[text_splitter]
)

# index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine(similarity_top_k=10)


question_answer_pairs = {
}

qa_prompt_tmpl_str = (
    """你是一个智能助手，请总结知识库的内容来回答问题，请列举知识库中的数据详细回答。
    先列出找到的文档，再说明原因。

当所有知识库内容都与问题无关时，你的回答必须包括“知识库中未找到您要的答案！”这句话。回答需要考虑聊天历史。
        以下是知识库：
        {{ context_str }}
        以上是知识库。"""
)
from llama_index.core.prompts import RichPromptTemplate
qa_prompt_tmpl = RichPromptTemplate(qa_prompt_tmpl_str)

query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
)

for question, answer in question_answer_pairs.items():
    response = query_engine.query(question)
    print("question:",question)
    print(response)
    print("参考文档:")
    file_names = set() # 对 v["file_name"] 进行去重
    for k,v in response.metadata.items():
        file_names.add(v["file_name"])
    for file_name in file_names:
        print(file_name)
    print("-"*100)


llm_4o = AzureOpenAI(
    model=eva_model,
    engine=eva_engine,
    api_key=eva_api_key,
    azure_endpoint=eva_azure_endpoint,
    api_version=eva_api_version,
)
evaluator = CorrectnessEvaluator(llm=llm)


