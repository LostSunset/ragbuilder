from typing import Callable
from enum import Enum
from importlib import import_module
from dataclasses import dataclass

@dataclass
class _PkgSpec:
    install_name: str
    import_name: str = ""
    
    def __post_init__(self):
        if not self.import_name:
            self.import_name = self.install_name.replace("-", "_")

    def validate(self) -> str:
        try:
            import_module(self.import_name)
            return ""
        except (ImportError, ModuleNotFoundError):
            return self.install_name

# Component type definitions
class GraphType(str, Enum):
    NEO4J = "neo4j"
    
class LLMType(str, Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"
    COHERE = "cohere"
    VERTEXAI = "vertexai"
    BEDROCK = "bedrock"
    JINA = "jina"
    CUSTOM = "custom"

class ParserType(str, Enum):
    UNSTRUCTURED = "unstructured"
    PYMUPDF = "pymupdf"
    PYPDF = "pypdf"
    DOCX = "docx"
    AZURE_BLOB = "azure_blob"
    S3 = "s3"
    DIRECTORY = "directory"
    WEB = "web"
    CUSTOM = "custom"

class ChunkingStrategy(str, Enum):
    CHARACTER = "CharacterTextSplitter"
    RECURSIVE = "RecursiveCharacterTextSplitter"
    TOKEN = "TokenTextSplitter"
    MARKDOWN = "MarkdownHeaderTextSplitter"
    HTML = "HTMLHeaderTextSplitter"
    SEMANTIC = "SemanticChunker"
    CUSTOM = "custom"

class EmbeddingModel(str, Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"
    COHERE = "cohere"
    VERTEXAI = "vertexai"
    BEDROCK = "bedrock"
    JINA = "jina"
    CUSTOM = "custom"

class VectorDatabase(str, Enum):
    FAISS = "faiss"
    CHROMA = "chroma"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"
    QDRANT = "qdrant"
    MILVUS = "milvus"
    PGVECTOR = "pgvector"
    ELASTICSEARCH = "elasticsearch"
    CUSTOM = "custom"

class RetrieverType(str, Enum):
    SIMILARITY = "similarity"
    MMR = "mmr"
    MULTI_QUERY = "multi_query"
    BM25 = "bm25"
    PARENT_DOC_RETRIEVER_FULL = "parent_doc_full"
    PARENT_DOC_RETRIEVER_LARGE = "parent_doc_large"
    GRAPH_RETRIEVER = "graph"
    CUSTOM = "custom"

class RerankerType(str, Enum):
    MXBAI_LARGE = "mixedbread-ai/mxbai-rerank-large-v1"
    MXBAI_BASE = "mixedbread-ai/mxbai-rerank-base-v1"
    BGE_BASE = "BAAI/bge-reranker-base"
    FLASH_RANK = "flashrank"
    COHERE = "cohere"
    JINA = "jina"
    COLBERT = "colbert"
    RANKLLM = "rankllm"
    CUSTOM = "custom"

class EvaluatorType(str, Enum):
    SIMILARITY = "similarity"
    RAGAS = "ragas"
    CUSTOM = "custom"

def lazy_load(module_path: str, class_name: str) -> Callable:
    """Lazy loader function that imports a class only when needed."""
    # def get_class():
    #     module = import_module(module_path)
    #     return getattr(module, class_name)
    # return get_class
    def get_class():
        try:
            # Dynamically import the module
            module = import_module(module_path)
            # Get the class from the module
            return getattr(module, class_name)
        except Exception as e:
            raise ValueError(f"Error loading {class_name} from module {module_path}: {e}")
    return get_class


# Component mappings with lazy loading
LLM_MAP = {
    LLMType.OPENAI: lazy_load("langchain_openai", "ChatOpenAI"),
    LLMType.AZURE_OPENAI: lazy_load("langchain_openai", "AzureChatOpenAI"),
}

LOADER_MAP = {
    ParserType.UNSTRUCTURED: lazy_load("langchain_community.document_loaders", "UnstructuredFileLoader"),
    ParserType.PYMUPDF: lazy_load("langchain_community.document_loaders", "PyMuPDFLoader"),
    ParserType.PYPDF: lazy_load("langchain_community.document_loaders", "PyPDFLoader"),
    ParserType.DOCX: lazy_load("langchain_community.document_loaders", "Docx2txtLoader"),
    ParserType.AZURE_BLOB: lazy_load("langchain_community.document_loaders", "AzureBlobStorageContainerLoader"),
    ParserType.S3: lazy_load("langchain_community.document_loaders", "S3DirectoryLoader"),
    ParserType.DIRECTORY: lazy_load("langchain_community.document_loaders", "DirectoryLoader"),
    ParserType.WEB: lazy_load("langchain_community.document_loaders", "WebBaseLoader"),
}

CHUNKER_MAP = {
    ChunkingStrategy.CHARACTER: lazy_load("langchain_text_splitters", "CharacterTextSplitter"),
    ChunkingStrategy.RECURSIVE: lazy_load("langchain_text_splitters", "RecursiveCharacterTextSplitter"),
    ChunkingStrategy.TOKEN: lazy_load("langchain_text_splitters", "TokenTextSplitter"),
    ChunkingStrategy.MARKDOWN: lazy_load("langchain_text_splitters", "MarkdownHeaderTextSplitter"),
    ChunkingStrategy.HTML: lazy_load("langchain_text_splitters", "HTMLHeaderTextSplitter"),
    ChunkingStrategy.SEMANTIC: lazy_load("langchain_experimental.text_splitter", "SemanticChunker"),
}

EMBEDDING_MAP = {
    EmbeddingModel.OPENAI: lazy_load("langchain_openai", "OpenAIEmbeddings"),
    EmbeddingModel.AZURE_OPENAI: lazy_load("langchain_openai", "AzureOpenAIEmbeddings"),
    EmbeddingModel.HUGGINGFACE: lazy_load("langchain_huggingface", "HuggingFaceEmbeddings"),
    EmbeddingModel.OLLAMA: lazy_load("langchain_community.embeddings", "OllamaEmbeddings"),
    EmbeddingModel.COHERE: lazy_load("langchain_community.embeddings", "CohereEmbeddings"),
    EmbeddingModel.VERTEXAI: lazy_load("langchain_community.embeddings", "VertexAIEmbeddings"),
    EmbeddingModel.BEDROCK: lazy_load("langchain_community.embeddings", "BedrockEmbeddings"),
    EmbeddingModel.JINA: lazy_load("langchain_community.embeddings", "JinaEmbeddings"),
}

VECTORDB_MAP = {
    VectorDatabase.FAISS: lazy_load("langchain.vectorstores", "FAISS"),
    VectorDatabase.CHROMA: lazy_load("langchain.vectorstores", "Chroma"),
    VectorDatabase.PINECONE: lazy_load("langchain.vectorstores", "Pinecone"),
    VectorDatabase.WEAVIATE: lazy_load("langchain.vectorstores", "Weaviate"),
    VectorDatabase.QDRANT: lazy_load("langchain.vectorstores", "Qdrant"),
    VectorDatabase.MILVUS: lazy_load("langchain.vectorstores", "Milvus"),
    VectorDatabase.PGVECTOR: lazy_load("langchain.vectorstores", "PGVector"),
    VectorDatabase.ELASTICSEARCH: lazy_load("langchain.vectorstores", "ElasticsearchStore"),
}

RETRIEVER_MAP = {
    RetrieverType.BM25: lazy_load("langchain.retrievers", "BM25Retriever"),
}

RERANKER_MAP = {
    RerankerType.MXBAI_LARGE: {
        'model_type': 'cross-encoder',
        'verbose': 0,
        'lazy_load': lazy_load("rerankers", "Reranker")
    },
    RerankerType.MXBAI_BASE: {
        'model_type': 'cross-encoder',
        'verbose': 0,
        'lazy_load': lazy_load("rerankers", "Reranker")
    },
    RerankerType.BGE_BASE: {
        'model_type': 'TransformerRanker',
        'verbose': 0,
        'lazy_load': lazy_load("rerankers", "Reranker")
    },
    RerankerType.FLASH_RANK: {
        'model_type': 'FlashRankRanker',
        'verbose': 0,
        'lazy_load': lazy_load("rerankers", "Reranker")
    },
    RerankerType.COHERE: {
        'model_type': 'APIRanker',
        'lang': 'en',
        'verbose': 0,
        'lazy_load': lazy_load("rerankers", "Reranker")
    },
    RerankerType.JINA: {
        'model_type': 'APIRanker',
        'verbose': 0,
        'lazy_load': lazy_load("rerankers", "Reranker")
    },
    RerankerType.COLBERT: {
        'model_type': 'ColBERTRanker',
        'verbose': 0,
        'lazy_load': lazy_load("rerankers", "Reranker")
    },
    RerankerType.RANKLLM: {
        'model_type': 'RankLLMRanker',
        'verbose': 0,
        'lazy_load': lazy_load("rerankers", "Reranker")
    },
    RerankerType.CUSTOM: {
        'lazy_load': lazy_load("rerankers", "Reranker")
    }
}

# Environment variable requirements for components
COMPONENT_ENV_REQUIREMENTS = {
    # Embedding Models
    EmbeddingModel.AZURE_OPENAI: {
        "required": ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"],
        "optional": ["AZURE_DEPLOYMENT_NAME"],
        "packages": [
            _PkgSpec("langchain-openai"),
            _PkgSpec("openai"),
            _PkgSpec("tiktoken")
        ]
    },
    EmbeddingModel.OPENAI: {
        "required": ["OPENAI_API_KEY"],
        "optional": [],
        "packages": [
            _PkgSpec("langchain-openai"),
            _PkgSpec("openai"),
            _PkgSpec("tiktoken")
        ]
    },
    EmbeddingModel.COHERE: {
        "required": ["COHERE_API_KEY"],
        "optional": [],
        "packages": [_PkgSpec("cohere")]
    },
    EmbeddingModel.VERTEXAI: {
        "required": ["GOOGLE_APPLICATION_CREDENTIALS"],
        "optional": [],
        "packages": [
            _PkgSpec("langchain-google-vertexai"),
            _PkgSpec("google-cloud-aiplatform")
        ]
    },
    EmbeddingModel.BEDROCK: {
        "required": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        "optional": [],
        "packages": [_PkgSpec("boto3")]
    },
    EmbeddingModel.JINA: {
        "required": ["JINA_API_KEY"],
        "optional": [],
        "packages": [_PkgSpec("jina")]
    },
    EmbeddingModel.HUGGINGFACE: {
        "required": [],
        "optional": [],
        "packages": [
            _PkgSpec("langchain-huggingface"),
            _PkgSpec("sentence_transformers"),
            _PkgSpec("torch")
        ]
    },
    EmbeddingModel.OLLAMA: {
        "required": [],
        "optional": [],
        "packages": [
            _PkgSpec("langchain-ollama"),
            _PkgSpec("ollama")
        ]
    },
    
    # Vector Databases
    VectorDatabase.PINECONE: {
        "required": ["PINECONE_API_KEY", "PINECONE_ENVIRONMENT"],
        "optional": [],
        "packages": [_PkgSpec("pinecone-client", "pinecone")]
    },
    VectorDatabase.WEAVIATE: {
        "required": ["WEAVIATE_URL", "WEAVIATE_API_KEY"],
        "optional": [],
        "packages": [_PkgSpec("weaviate-client", "weaviate")]
    },
    VectorDatabase.QDRANT: {
        "required": ["QDRANT_URL"],
        "optional": ["QDRANT_API_KEY"],
        "packages": [_PkgSpec("qdrant-client", "qdrant")]
    },
    VectorDatabase.MILVUS: {
        "required": ["MILVUS_HOST", "MILVUS_PORT"],
        "optional": [],
        "packages": [_PkgSpec("pymilvus")]
    },
    VectorDatabase.PGVECTOR: {
        "required": ["PGVECTOR_CONNECTION_STRING"],
        "optional": [],
        "packages": [
            _PkgSpec("psycopg2-binary"),
            _PkgSpec("pgvector")
        ]
    },
    VectorDatabase.ELASTICSEARCH: {
        "required": ["ELASTICSEARCH_URL"],
        "optional": ["ELASTICSEARCH_API_KEY"],
        "packages": [_PkgSpec("elasticsearch")]
    },
    VectorDatabase.CHROMA: {
        "required": [],
        "optional": [],
        "packages": [_PkgSpec("chromadb")]
    },
    VectorDatabase.FAISS: {
        "required": [],
        "optional": [],
        "packages": [_PkgSpec("faiss-cpu")]
    },
    
    # Document Loaders
    ParserType.UNSTRUCTURED: {
        "required": [],
        "optional": [],
        "packages": [_PkgSpec("unstructured")]
    },
    ParserType.PYMUPDF: {
        "required": [],
        "optional": [],
        "packages": [_PkgSpec("pymupdf")]
    },
    ParserType.PYPDF: {
        "required": [],
        "optional": [],
        "packages": [_PkgSpec("pypdf")]
    },
    ParserType.DOCX: {
        "required": [],
        "optional": [],
        "packages": [_PkgSpec("python-docx", "docx")]
    },
    ParserType.AZURE_BLOB: {
        "required": ["AZURE_STORAGE_CONNECTION_STRING"],
        "optional": [],
        "packages": [_PkgSpec("azure-storage-blob")]
    },
    ParserType.S3: {
        "required": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        "optional": [],
        "packages": [_PkgSpec("boto3")]
    },
    ParserType.WEB: {
        "required": [],
        "optional": [],
        "packages": [
            _PkgSpec("beautifulsoup4", "bs4"),
            _PkgSpec("requests")
        ]
    },
    
    RetrieverType.BM25: {
        "required": [],
        "optional": [],
        "packages": [_PkgSpec("rank-bm25")]
    },

    # Rerankers
    RerankerType.COHERE: {
        "required": ["COHERE_API_KEY"],
        "optional": [],
        "packages": [_PkgSpec("cohere")]
    },
    RerankerType.JINA: {
        "required": ["JINA_API_KEY"],
        "optional": [],
        "packages": [_PkgSpec("jina")]
    },
    RerankerType.RANKLLM: {
        "required": [],
        "optional": [],
        "packages": [_PkgSpec("rank-llm")]
    },
    RerankerType.MXBAI_LARGE: {
        "required": [],
        "optional": [],
        "packages": [
            _PkgSpec("torch"),
            _PkgSpec("transformers")
        ]
    },
    RerankerType.MXBAI_BASE: {
        "required": [],
        "optional": [],
        "packages": [
            _PkgSpec("torch"),
            _PkgSpec("transformers")
        ]
    },
    RerankerType.BGE_BASE: {
        "required": [],
        "optional": [],
        "packages": [
            _PkgSpec("torch"),
            _PkgSpec("transformers")
        ]
    },
    RerankerType.FLASH_RANK: {
        "required": [],
        "optional": [],
        "packages": [_PkgSpec("flash-rank")]
    }
}