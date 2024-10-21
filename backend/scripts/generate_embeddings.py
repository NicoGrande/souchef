from google.cloud import bigquery
from langchain_community.embeddings import OpenAIEmbeddings
import langchain.text_splitter as text_splitter
import logging
import pandas as pd
import os
import getpass
from tqdm import tqdm


logging.basicConfig(level=logging.INFO)


def query_food_data(project_id: str = "souschef-d4403") -> pd.DataFrame:
    """Query the branded food description data from BigQuery.

    Args:
        project_id (str): The Google Cloud project ID. Defaults to "souschef-d4403".

    Returns:
        pd.DataFrame: A DataFrame containing the queried food data.
    """
    logging.info(f"Querying {project_id}.food_data.branded_food_description")

    client = bigquery.Client(project=project_id)
    query = """
    SELECT * FROM `souschef-d4403.food_data.branded_food_description`
    """
    food_df = client.query_and_wait(query).to_dataframe()
    return food_df


def split_descriptions(food_df: pd.DataFrame) -> pd.DataFrame:
    """Split food descriptions into smaller chunks.

    Args:
        food_df (pd.DataFrame): DataFrame containing food data with descriptions.

    Returns:
        pd.DataFrame: A DataFrame with split descriptions, containing 'fdc_id' and 'text' columns.
    """
    logging.info(f"Splitting {len(food_df)} descriptions into chunks")
    splitter = text_splitter.RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=0
    )
    chunks = []
    for _, row in tqdm(food_df.iterrows(), total=len(food_df), desc="Splitting descriptions"):
        splits = splitter.create_documents([row["description"]])
        [
            chunks.append({"fdc_id": row["fdc_id"], "text": split.page_content})
            for split in splits
        ]

    return pd.DataFrame(chunks)


def generate_embeddings(chunked_df: pd.DataFrame, batch_size: int = 100) -> pd.DataFrame:
    """Generate embeddings for the chunked descriptions.

    Args:
        chunked_df (pd.DataFrame): DataFrame containing chunked descriptions.
        batch_size (int): Number of rows to process in each batch. Defaults to 100.

    Returns:
        pd.DataFrame: A DataFrame with generated embeddings added as a new column.
    """
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    logging.info(f"Generating embeddings for {len(chunked_df)} chunks in batches of {batch_size}")
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    
    result_df = pd.DataFrame()
    for i in tqdm(range(0, len(chunked_df), batch_size), desc="Generating embeddings"):
        batch = chunked_df.iloc[i:i+batch_size]
        batch["embedding"] = batch["text"].apply(lambda x: embedding.embed_query(x))
        result_df = pd.concat([result_df, batch], ignore_index=True)
        
        # Save intermediate results
        save_embeddings(result_df, table_id="food_embeddings")
        
    return result_df


def save_embeddings(
    embeddings_df: pd.DataFrame,
    project_id: str = "souschef-d4403",
    dataset_id: str = "food_data",
    table_id: str = "food_embeddings",
) -> None:
    """Save the generated embeddings to a BigQuery table.

    Args:
        embeddings_df (pd.DataFrame): DataFrame containing the embeddings to be saved.
        project_id (str): The Google Cloud project ID. Defaults to "souschef-d4403".
        dataset_id (str): The BigQuery dataset ID. Defaults to "food_data".
        table_id (str): The BigQuery table ID. Defaults to "food_embeddings".

    Returns:
        None
    """
    logging.info(f"Appending {len(embeddings_df)} embeddings to {dataset_id}.{table_id}")
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    
    # Configure the load job to append data
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]
    )
    
    job = client.load_table_from_dataframe(embeddings_df, table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete

    # Log the number of rows in the table after appending
    table = client.get_table(table_ref)
    logging.info(f"Total rows in {dataset_id}.{table_id} after appending: {table.num_rows}")


if __name__ == "__main__":
    food_df = query_food_data()
    chunked_df = split_descriptions(food_df)
    embeddings_df = generate_embeddings(chunked_df)
    save_embeddings(embeddings_df)
