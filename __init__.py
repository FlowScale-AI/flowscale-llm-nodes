print("Initializing Flowscale LLM Nodes")

from .nodes.llm.openai import OpenAIAPI
from .nodes.llm.openai_node_input import OpenAIAPIWithAPIKey
from .nodes.llm.brand_voice import OpenAIBrandVoiceReformatter
from .nodes.embedding.openai import OpenAIEmbedding
from .nodes.vectordb.astradb import AstraDBStoreEmbeddingsNode
from .nodes.vectordb import AstraOpenAISearchNode, AstraOpenAIIngestNode

from .utilitynodes.fileloader import FileLoaderNode
from .utilitynodes.json_extracter import ExtractPropertyNode
from .utilitynodes.webhook import WebhookSender

NODE_CLASS_MAPPINGS = {
  "openai": OpenAIAPI,
  "openai_with_api_key": OpenAIAPIWithAPIKey,
  "openai_brand_voice_reformatter": OpenAIBrandVoiceReformatter,
  "openai_embedding": OpenAIEmbedding,
  "astradb_store_embeddings": AstraDBStoreEmbeddingsNode,
  "astradb_search": AstraOpenAISearchNode,
  "astradb_ingest": AstraOpenAIIngestNode,
  
  "json_extract_property": ExtractPropertyNode,
  "file_loader": FileLoaderNode,
  "webhook_sender": WebhookSender
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "openai": "[FS] OpenAI",
  "openai_with_api_key": "[FS] OpenAI (with API Key)",
  "openai_brand_voice_reformatter": "[FS] OpenAI Brand Voice Reformatter",
  "openai_embedding": "[FS] OpenAI Embedding",
  "astradb_store_embeddings": "[FS] AstraDB Store Embeddings",
  "astradb_search": "[FS] AstraDB Search",
  "astradb_ingest": "[FS] AstraDB Ingest",
  
  "file_loader": "[FS] File Loader",
  "json_extract_property": "[FS] JSON Extract Property",
  "webhook_sender": "[FS] Webhook"
}