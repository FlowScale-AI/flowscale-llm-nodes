import json
import os
import requests
from typing import Tuple
from openai import OpenAI
from astrapy import DataAPIClient
import dotenv
import logging

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#####################
# Astra + OpenAI Node
#####################
class AstraOpenAISearchNode:
    """
    This node takes a string input, uses OpenAI to embed it,
    and queries an Astra DB Vector Store for similar documents.
    It returns the JSON string of matched documents.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "search_query": ("STRING", {"multiline": False, "default": ""}),
                "astradb_token": ("STRING", {"multiline": False, "default": ""}),
                "astradb_endpoint": ("STRING", {"multiline": False, "default": ""}),
                "collection_name": ("STRING", {"multiline": False, "default": ""}),
                "conversation_id": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    # ComfyUI expects you to define what the node returns
    RETURN_TYPES = ("STRING",)  # We'll return a JSON string
    FUNCTION = "search_astra"
    CATEGORY = "Astra / Search"  # or whatever category you prefer

    def search_astra(
        self,
        search_query: str,
        astradb_token: str,
        astradb_endpoint: str,
        collection_name: str,
        conversation_id: str
    ) -> Tuple[str]:
        """
        Main function for the node. Generates an embedding using OpenAI, 
        then sends the embedding to Astra DB to do a similarity search.
        Returns the JSON string of search results.
        """
        # 1) Generate Embedding with OpenAI
        embedding = self._generate_openai_embedding(search_query)
        logger.info(f"Generated embedding: {embedding}")
        # 2) Search in Astra DB
        #    Since we don't have an out-of-the-box "AstraDBVectorStore" import here, 
        #    you'd do one of two things:
        #    a) Use an external library like langchain_astradb (then call vector_store.search(...)).
        #    b) Use the Astra REST API to do a similarity search with your custom setup.

        # For demonstration, let's do the simpler "direct REST to Astra" approach:
        results = self._search_astra_by_embedding(
            astradb_token, 
            astradb_endpoint, 
            collection_name, 
            embedding,
            conversation_id
            # keyspace,
            # top_k
        )

        # 3) Return as a string joining list contents
        
        search_output = [
            {
                "content": result.get("content"),
                "timestamp": result.get("timestamp"),
            }
            for result in results
        ]
        
        sorted_search_output = sorted(search_output, key=lambda x: x["timestamp"], reverse=True)
        
        return (json.dumps(search_output),)

    def _generate_openai_embedding(self, text: str, embedding_model: str = "text-embedding-3-small"):
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        if not openai_api_key:
            logger.info("OpenAI API key not set")
            return "OpenAI API key not set"
        
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        
        text = text.replace("\n", " ")
        return client.embeddings.create(input=[text], model=embedding_model).data[0].embedding

    def _search_astra_by_embedding(
        self,
        astradb_token: str,
        astradb_endpoint: str,
        collection_name: str,
        query_embedding: list,
        conversation_id: str,
        keyspace: str = "",
        # top_k: int = 4
    ):
        client = DataAPIClient(astradb_token)
        db = client.get_database_by_api_endpoint(astradb_endpoint)
        
        collection = db.get_collection(collection_name)
        
        results = collection.find(
          {"conversation_id": conversation_id},
          sort={"timestamp": -1},
        )
        
        result_list = []
        for result in results:
            logger.info(f"Found document: {result}")
            result_list.append(result)
        
        return result_list
        