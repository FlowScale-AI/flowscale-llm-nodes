import os
import json
import requests
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_astradb import AstraDBVectorStore
from astrapy.admin import parse_api_endpoint

class AstraDBStoreEmbeddingsNode:
    """
    A ComfyUI node for storing text documents as vector embeddings in Astra DB.
    
    This node:
    1) Takes string input (text).
    2) Uses an OpenAI Embedding model to generate embeddings.
    3) Stores the embeddings in a specified Astra DB collection.
    4) Returns a status string for success or failure.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_data": ("STRING", {"multiline": True}),
                "astra_token": ("STRING", {}),
                "astra_api_endpoint": ("STRING", {}),
                "collection_name": ("STRING", {}),
            },
            "optional": {
                "openai_api_key": ("STRING", {}),     # If you want to supply a custom OpenAI key
                "keyspace": ("STRING", {}),          # Optional Astra DB keyspace (namespace)
                "metadata_json": ("STRING", {"multiline": True}),  # Additional metadata in JSON format
                "silent_errors": ("BOOLEAN",),       # Toggle silent/fail-hard mode
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "store_embeddings"
    CATEGORY = "VectorDB"

    def store_embeddings(
        self,
        text_data,
        astra_token,
        astra_api_endpoint,
        collection_name,
        openai_api_key=None,
        keyspace=None,
        metadata_json="{}",
        silent_errors=True
    ):
        """
        Generates embeddings for the provided text, then stores them in Astra DB.
        """
        # 1. Validate text content
        if not text_data.strip():
            if silent_errors:
                return ("No text provided.",)
            raise ValueError("No text data provided for embeddings.")

        # 2. Set OpenAI API key if provided
        if openai_api_key and openai_api_key.strip():
            os.environ["OPENAI_API_KEY"] = openai_api_key.strip()
        elif os.getenv("OPENAI_API_KEY") is None:
            if silent_errors:
                return ("OpenAI API key not set, and silent_errors=True. Skipping embedding...",)
            raise ValueError("OpenAI API key is not set. Provide one or set OPENAI_API_KEY in env.")

        # 3. Prepare metadata
        try:
            doc_metadata = json.loads(metadata_json) if metadata_json.strip() else {}
        except Exception as e:
            if silent_errors:
                return (f"Invalid metadata JSON. Error: {e}",)
            raise ValueError(f"Failed to parse metadata JSON: {e}")

        document = Document(page_content=text_data, metadata=doc_metadata)

        # 4. Generate embeddings using OpenAI
        try:
            embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
        except Exception as e:
            if silent_errors:
                return (f"Failed to initialize OpenAI embeddings: {e}",)
            raise ValueError(f"Failed to initialize OpenAI embeddings: {e}")

        # 5. Initialize AstraDBVectorStore
        try:
            parsed_endpoint = parse_api_endpoint(astra_api_endpoint)
            vector_store = AstraDBVectorStore(
                collection_name=collection_name,
                token=astra_token,
                api_endpoint=astra_api_endpoint,
                namespace=keyspace,
                environment=parsed_endpoint.environment if parsed_endpoint else None,
                embedding=embedding_model,
            )
        except Exception as e:
            if silent_errors:
                return (f"Failed to initialize AstraDBVectorStore: {e}",)
            raise ValueError(f"Failed to initialize AstraDBVectorStore: {e}")

        # 6. Add document t
