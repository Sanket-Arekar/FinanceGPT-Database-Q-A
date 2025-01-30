from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseSequentialChain
from langchain_experimental.sql import SQLDatabaseChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
import os
from few_shots import FewShotsCache

load_dotenv()

#Create LLM Object
llm = ChatOpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"], model_name='gpt-3.5-turbo')


def get_few_shot_db_chain():
    # Create DB Object
    db_user = "root"
    db_password = "password"
    db_host = "localhost"
    db_name = "financial_insights_large"

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                              sample_rows_in_table_info=3)

    print(db.table_info)


    #Creating Few Shots
    # few_shots = create_few_shots(llm,db)
    # Usage
    few_shots_cache = FewShotsCache()
    few_shots = few_shots_cache.initialize_few_shots(llm, db)

    #Create Embeddings using HuggingFace
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L12-v2')

    # Now create chunks of the few shots.
    # Here we will combine all the values from the few_shots into a blob.
    to_vectorize = [" ".join(example.values()) for example in few_shots]

    # Creatinga Vector Store
    # Process small batches instead of all at once
    batch_size = 10  # Adjust based on memory constraints
    for i in range(0, len(to_vectorize), batch_size):
        batch_texts = to_vectorize[i:i + batch_size]
        batch_metadatas = few_shots[i:i + batch_size]
        vectorstore = Chroma.from_texts(batch_texts, embeddings, metadatas=batch_metadatas,
                                        persist_directory="./chroma_db")

    vectorstore.persist()  # Ensures the data is stored on disk

    #Creating a Similarity Example Selector
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )

    ### my sql based instruction prompt
    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".

    Use the following format:

    Question: Question here
    SQLQuery: Query to run with no pre-amble
    SQLResult: Result of the SQLQuery
    Answer: Final answer here

    No pre-amble.
    """

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer", ],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],  # These variables are used in the prefix and suffix
    )

    new_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
    return new_chain

if __name__ == "__main__":
    chain = get_few_shot_db_chain()
    print(chain.run("find the day in 2023 with the highest revenue."))
