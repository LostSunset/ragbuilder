from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Union, Dict, Any
import yaml
import time
import random
import logging
from dataclasses import dataclass
from .components import ParserType, ChunkingStrategy, EmbeddingModel, VectorDatabase, EvaluatorType

@dataclass
class LogConfig:
    """Configuration for logging"""
    log_level: int = logging.INFO
    log_file: Optional[str] = None
    show_progress_bar: bool = True
    verbose: bool = False

class LoaderConfig(BaseModel):
    type: ParserType
    loader_kwargs: Optional[Dict[str, Any]] = None
    custom_class: Optional[str] = None

class ChunkingStrategyConfig(BaseModel):
    type: ChunkingStrategy
    chunker_kwargs: Optional[Dict[str, Any]] = None
    custom_class: Optional[str] = None

class ChunkSizeConfig(BaseModel):
    min: int = Field(default=100, description="Minimum chunk size")
    max: int = Field(default=500, description="Maximum chunk size")
    stepsize: int = Field(default=100, description="Step size for chunk size")

class VectorDBConfig(BaseModel):
    type: VectorDatabase
    vectordb_kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Vector database specific configuration parameters")
    custom_class: Optional[str] = None

class EmbeddingConfig(BaseModel):
    type: EmbeddingModel
    model_kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Model specific parameters including model name/type")
    custom_class: Optional[str] = None

class EvaluationConfig(BaseModel):
    type: EvaluatorType = Field(default=EvaluatorType.SIMILARITY, description="Type of evaluator to use")
    custom_class: Optional[str] = Field(default=None, description="Path to custom evaluator class")
    evaluator_kwargs: Optional[Dict[str, Any]] = Field(
        default = {
            "top_k": 5,
            "position_weights": None,
            "relevance_threshold": 0.75
        },
        description="Additional parameters for evaluator initialization"
    )

class OptimizationConfig(BaseModel):
    type: Optional[str] = "Optuna"
    n_trials: Optional[int] = Field(default=10, description="Number of trials for optimization")
    n_jobs: Optional[int] = Field(default=1, description="Number of jobs for optimization")
    timeout: Optional[int] = Field(default=None, description="Timeout for optimization")
    storage: Optional[str] = Field(default=None, description="Storage URL for Optuna (e.g., 'sqlite:///optuna.db')")
    study_name: Optional[str] = Field(default=f"data_ingest_{int(time.time()*1000+random.randint(1, 1000))}", description="Name of the Optuna study")
    load_if_exists: Optional[bool] = Field(default=False, description="Load existing study if it exists")
    overwrite_study: Optional[bool] = Field(default=False, description="Overwrite existing study if it exists")
    optimization_direction: Optional[str] = Field(default="maximize", description="Whether to maximize or minimize the optimization metric")

class BaseConfig(BaseModel):
    input_source: Union[str, List[str]] = Field(..., description="File path, directory path, or URL for input data")
    test_dataset: str = Field(..., description="Path to CSV file containing test questions")

    @classmethod
    def from_yaml(cls, file_path: str) -> 'DataIngestConfig':
        """
        Load configuration from a YAML file.
        """
        with open(file_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        return cls(**config_dict)

    def to_yaml(self, file_path: str) -> None:
        """
        Save configuration to a YAML file.
        """
        with open(file_path, 'w') as file:
            yaml.dump(self.model_dump(), file)

class DataIngestOptionsConfig(BaseConfig):
    document_loaders: Optional[List[LoaderConfig]] = Field(
        default_factory=lambda: [LoaderConfig(type=ParserType.UNSTRUCTURED)], 
        description="Document loader configurations"
    )
    chunking_strategies: Optional[List[ChunkingStrategyConfig]] = Field(
        default_factory=lambda: [ChunkingStrategyConfig(type=ChunkingStrategy.RECURSIVE)],
        description="Chunking strategies to try"
    )
    chunk_size: Optional[ChunkSizeConfig] = Field(default_factory=ChunkSizeConfig, description="Chunk size configuration")
    chunk_overlap: Optional[List[int]] = Field(default=[100], description="List of chunk overlap values to try")
    embedding_models: Optional[List[EmbeddingConfig]] = Field(
        default_factory=lambda: [EmbeddingConfig(type=EmbeddingModel.HUGGINGFACE, model_kwargs={"model_name": "sentence-transformers/all-MiniLM-L6-v2"})],
        description="List of embedding models"
    )
    vector_databases: Optional[List[VectorDBConfig]] = Field(
        default_factory=lambda: [VectorDBConfig(type=VectorDatabase.FAISS, vectordb_kwargs={})], 
        description="List of vector databases"
    )
    sampling_rate: Optional[float] = Field(default=None, description="Sampling rate for documents (0.0 to 1.0). None or 1.0 means no sampling.")
    optimization: Optional[OptimizationConfig] = Field(default_factory=OptimizationConfig, description="Optimization configuration")
    log_config: Optional[LogConfig] = Field(default_factory=LogConfig, description="Logging configuration")
    database_logging: Optional[bool] = Field(default=True, description="Whether to log results to the DB")
    database_path: Optional[str] = Field(default="eval.db", description="Path to the SQLite database file")
    evaluation_config: EvaluationConfig = Field(
        default_factory=lambda: EvaluationConfig(
            type=EvaluatorType.SIMILARITY,
            evaluator_kwargs={
                "top_k": 5,
                "position_weights": None,
                "relevance_threshold": 0.75
            }
        ),
        description="Evaluation configuration"
    )

class DataIngestConfig(BaseConfig):
    document_loader: LoaderConfig = Field(
        default_factory=lambda: LoaderConfig(type=ParserType.UNSTRUCTURED), 
        description="Document loader configuration"
    )
    chunking_strategy: ChunkingStrategyConfig = Field(default_factory=lambda: ChunkingStrategyConfig(type=ChunkingStrategy.RECURSIVE), description="Chunking strategy")
    chunk_size: int = Field(default=1000, description="Chunk size")
    chunk_overlap: int = Field(default=100, description="Chunk overlap")
    embedding_model: EmbeddingConfig = Field(
        default_factory=lambda: EmbeddingConfig(type=EmbeddingModel.HUGGINGFACE, model_kwargs={"model_name": "sentence-transformers/all-MiniLM-L6-v2"}), 
        description="Embedding model configuration"
    )
    vector_database: VectorDBConfig = Field(
        default_factory=lambda: VectorDBConfig(type=VectorDatabase.FAISS, vectordb_kwargs={}), 
        description="Vector store configuration"
    )
    sampling_rate: Optional[float] = Field(default=None, description="Sampling rate for documents (0.0 to 1.0). None or 1.0 means no sampling.")

def load_config(file_path: str) -> Union[DataIngestOptionsConfig, DataIngestConfig]:
    with open(file_path, 'r') as file:
        config_dict = yaml.safe_load(file)
    
    # Check for required fields
    if 'input_source' not in config_dict or 'test_dataset' not in config_dict:
        raise ValueError("Configuration must include 'input_source' and 'test_data'")
    
    # TODO: Re-think and redo this logic to see if there's a better way
    try:
        return DataIngestOptionsConfig(**config_dict)
    except ValidationError:
        # If it fails, try DataIngestConfig
        try:
            return DataIngestConfig(**config_dict)
        except ValidationError as e:
            raise ValueError(f"Invalid configuration: {str(e)}")

def save_config(config: Union[DataIngestOptionsConfig, DataIngestConfig], file_path: str) -> None:
    """
    Save configuration to a YAML file.
    """
    config.to_yaml(file_path)