from google.cloud import bigquery
import langchain.embeddings as embeddings
import langchain.text_splitter as text_splitter
import pandas as pd
import os
import getpass


def query_food_data(project_id: str = "souschef-d4403") -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    query = """
    SELECT * FROM `souschef-d4403.food_data.branded_food_description` LIMIT 10
    """
    food_df = client.query_and_wait(query).to_dataframe()
    return food_df


def split_descriptions(food_df: pd.DataFrame) -> pd.DataFrame:
    splitter = text_splitter.RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=0
    )
    chunks = []
    for _, row in food_df.iterrows():
        splits = splitter.create_documents([row["description"]])
        [
            chunks.append({"fdc_id": row["fdc_id"], "text": split.page_content})
            for split in splits
        ]

    return pd.DataFrame(chunks)


def generate_embeddings(chunked_df: pd.DataFrame) -> pd.DataFrame:
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    embedding = embeddings.OpenAIEmbeddings(model="text-embedding-3-small")
    chunked_df["embedding"] = chunked_df["text"].apply(
        lambda x: embedding.embed_query(x)
    )
    return chunked_df


def save_embeddings(
    embeddings_df: pd.DataFrame,
    project_id: str = "souschef-d4403",
    dataset_id: str = "food_data",
    table_id: str = "food_embeddings",
) -> None:
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job = client.load_table_from_dataframe(embeddings_df, table_ref)
    job.result()


if __name__ == "__main__":
    food_df = query_food_data()
    chunked_df = split_descriptions(food_df)
    embeddings_df = generate_embeddings(chunked_df)
    save_embeddings(embeddings_df)
