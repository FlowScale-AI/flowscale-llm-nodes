# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **ComfyUI custom nodes library** called "Flowscale LLM Nodes" that provides LLM, embedding, vector database, and utility nodes for visual workflow building. The nodes follow ComfyUI's pattern of defining `INPUT_TYPES`, `RETURN_TYPES`, `FUNCTION`, and `CATEGORY` class attributes.

## Architecture

### Node System Pattern

All nodes follow this structure:
- `INPUT_TYPES(cls)`: Class method returning dict with "required" and optional "optional" input parameters
- `RETURN_TYPES`: Tuple of output type strings (e.g., `("STRING",)`)
- `RETURN_NAMES`: Optional tuple of output names
- `FUNCTION`: String name of the method to execute
- `CATEGORY`: String for UI categorization

Node methods always return tuples, even for single values: `return (result,)`

### Node Registry

`__init__.py` maintains two dictionaries:
- `NODE_CLASS_MAPPINGS`: Maps node IDs to classes
- `NODE_DISPLAY_NAME_MAPPINGS`: Maps node IDs to display names (prefixed with `[FS]`)

When adding new nodes, register them in both dictionaries.

### Module Organization

- **`nodes/llm/`**: LLM API nodes (OpenAI, brand voice reformatting)
  - `OpenAIAPI`: Uses env `OPENAI_API_KEY`
  - `OpenAIAPIWithAPIKey`: Accepts API key as parameter
  - `OpenAIBrandVoiceReformatter`: Rewrites text in specified brand voice

- **`nodes/embedding/`**: Embedding generation nodes
  - `OpenAIEmbedding`: Creates embeddings using OpenAI models

- **`nodes/vectordb/`**: Astra DB vector database nodes
  - `AstraDBStoreEmbeddingsNode`: Stores embeddings using LangChain integration
  - `AstraOpenAIIngestNode`: Ingests text chunks with embeddings into Astra DB
  - `AstraOpenAISearchNode`: Searches Astra DB by conversation_id (note: embedding generation is currently disabled)

- **`utilitynodes/`**: General utility nodes
  - `FileLoaderNode`: Loads files from URLs (supports PDF and text)
  - `ExtractPropertyNode`: Extracts properties from JSON strings
  - `WebhookSender`: Sends data to webhooks

### Key Dependencies

- `openai`: OpenAI API client
- `langchain`, `langchain_community`, `langchain-astradb`: LangChain integrations
- `astrapy`: Astra DB Data API client
- `PyPDF2`: PDF processing
- `python-dotenv`: Environment variable loading

All nodes use `dotenv.load_dotenv()` to load environment variables.

### Environment Variables

- `OPENAI_API_KEY`: Required for OpenAI LLM and embedding nodes (unless passed as parameter)
- `ASTRA_DB_APPLICATION_TOKEN`: Fallback for Astra DB authentication
- `ASTRA_DB_API_ENDPOINT`: Fallback for Astra DB endpoint

### API Key Handling Pattern

Most nodes follow this pattern:
1. Check for API key parameter (if supported)
2. Fall back to environment variable
3. Return error tuple if missing: `return ("API key not set",)`

### Error Handling

Many nodes support a `silent_errors` boolean parameter:
- When `True`: Returns error message as tuple
- When `False`: Raises `ValueError`

### Astra DB Integration

Two different patterns exist:

1. **LangChain-based** (`astradb.py`): Uses `AstraDBVectorStore` from `langchain-astradb`
2. **Direct API** (`astradb_ingest.py`, `astradb_search.py`): Uses `DataAPIClient` from `astrapy`

The direct API pattern stores documents with:
- `content`: Text chunk
- `conversation_id`: Conversation identifier for filtering
- `timestamp`: ISO format timestamp
- `$vector`: Embedding vector

Search in `astradb_search.py` currently filters by `conversation_id` without vector similarity (line 55: `embedding = []`).

## Development Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_key_here
ASTRA_DB_APPLICATION_TOKEN=your_token_here
ASTRA_DB_API_ENDPOINT=your_endpoint_here
```

## Adding New Nodes

1. Create node class in appropriate module directory
2. Implement required class attributes: `INPUT_TYPES`, `RETURN_TYPES`, `FUNCTION`, `CATEGORY`
3. Implement the function method (must return tuple)
4. Import in `__init__.py`
5. Add to both `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`
6. Use `[FS]` prefix in display name for consistency
