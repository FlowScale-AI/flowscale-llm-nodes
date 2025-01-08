print("Hello")

from .nodes.llm.openai import OpenAIAPI
from .nodes.embedding.openai import OpenAIEmbedding
from .nodes.vectordb.astradb import AstraDBStoreEmbeddingsNode

from .utilitynodes.fileloader import FileLoaderNode

NODE_CLASS_MAPPINGS = {
  "openai": OpenAIAPI,
  "openai_embedding": OpenAIEmbedding,
  "astradb_store_embeddings": AstraDBStoreEmbeddingsNode,
  
  "file_loader": FileLoaderNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "openai": "[FS] OpenAI",
  "openai_embedding": "[FS] OpenAI Embedding",
  "astradb_store_embeddings": "[FS] AstraDB Store Embeddings",
  
  "file_loader": "[FS] File Loader"
}