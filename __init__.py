from .nodes.llm.openai import OpenAIAPI
from .nodes.llm.brand_voice import OpenAIBrandVoiceReformatter
from .nodes.embedding.openai import OpenAIEmbedding
from .nodes.vectordb.astradb import AstraDBStoreEmbeddingsNode
from .nodes.vectordb.astradb_search import AstraOpenAISearchNode

from .utilitynodes.fileloader import FileLoaderNode
from .utilitynodes.json_extracter import ExtractPropertyNode
from .utilitynodes.webhook import WebhookSender

NODE_CLASS_MAPPINGS = {
  "openai": OpenAIAPI,
  "openai_brand_voice_reformatter": OpenAIBrandVoiceReformatter,
  "openai_embedding": OpenAIEmbedding,
  "astradb_store_embeddings": AstraDBStoreEmbeddingsNode,
  "astradb_search": AstraOpenAISearchNode,
  
  "json_extract_property": ExtractPropertyNode,
  "file_loader": FileLoaderNode,
  "webhook_sender": WebhookSender
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "openai": "[FS] OpenAI",
  "openai_brand_voice_reformatter": "[FS] OpenAI Brand Voice Reformatter",
  "openai_embedding": "[FS] OpenAI Embedding",
  "astradb_store_embeddings": "[FS] AstraDB Store Embeddings",
  "astradb_search": "[FS] AstraDB Search",
  
  "file_loader": "[FS] File Loader",
  "json_extract_property": "[FS] JSON Extract Property",
  "webhook_sender": "[FS] Webhook"
}