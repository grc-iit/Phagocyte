"""LanceDB table schemas."""


# Schema definitions as dictionaries for LanceDB
# LanceDB will create tables with these columns

def get_text_chunk_schema(vector_dims: int = 1024) -> dict:
    """Get schema for text/paper chunks table.

    Args:
        vector_dims: Dimension of embedding vectors

    Returns:
        Schema dictionary for table creation
    """
    return {
        "id": "string",
        "content": "string",
        "content_hash": "string",
        "vector": f"vector[{vector_dims}]",
        "source_file": "string",
        "source_type": "string",
        "start_line": "int32",
        "end_line": "int32",
        "start_char": "int32",
        "end_char": "int32",
        "parent_id": "string",
        "title": "string",
        "section_path": "string",
        "citations": "string",  # JSON array
        "token_count": "int32",
    }


def get_code_chunk_schema(vector_dims: int = 768) -> dict:
    """Get schema for code chunks table.

    Args:
        vector_dims: Dimension of embedding vectors

    Returns:
        Schema dictionary for table creation
    """
    return {
        "id": "string",
        "content": "string",
        "content_hash": "string",
        "vector": f"vector[{vector_dims}]",
        "source_file": "string",
        "source_type": "string",
        "language": "string",
        "start_line": "int32",
        "end_line": "int32",
        "start_char": "int32",
        "end_char": "int32",
        "parent_id": "string",
        "symbol_name": "string",
        "symbol_type": "string",
        "imports": "string",  # JSON array
        "token_count": "int32",
    }


def get_unified_chunk_schema(vector_dims: int = 1024) -> dict:
    """Get schema for unified chunks table.

    For multimodal unified tables, use CLIP/SigLIP dimensions (1024 or 1152)
    to enable cross-modal search (text can find images and vice versa).

    Args:
        vector_dims: Dimension of embedding vectors (default 1024 for CLIP)

    Returns:
        Schema dictionary for table creation
    """
    return {
        "id": "string",
        "content": "string",
        "content_hash": "string",
        "vector": f"vector[{vector_dims}]",
        "source_file": "string",
        "source_type": "string",  # ContentType value
        "content_type": "string",  # 'text', 'code', 'paper', 'image'
        "language": "string",
        "start_line": "int32",
        "end_line": "int32",
        "parent_id": "string",
        "title": "string",
        "section_path": "string",
        "symbol_name": "string",
        "symbol_type": "string",
        "metadata_json": "string",  # Additional metadata as JSON
        "token_count": "int32",
    }


def get_image_chunk_schema(
    text_vector_dims: int = 1024,
    visual_vector_dims: int = 1024,
) -> dict:
    """Get schema for image chunks table.

    Image chunks have TWO vector columns:
    - text_vector: Embedding of the VLM-generated description
    - visual_vector: CLIP/SigLIP embedding of the actual image

    Args:
        text_vector_dims: Dimension of text embeddings (stella: 1024)
        visual_vector_dims: Dimension of visual embeddings (CLIP: 1024)

    Returns:
        Schema dictionary for table creation
    """
    return {
        "id": "string",
        "figure_id": "int32",
        "caption": "string",
        "vlm_description": "string",
        "classification": "string",
        "page": "int32",
        "image_path": "string",
        "source_paper": "string",
        "text_vector": f"vector[{text_vector_dims}]",
        "visual_vector": f"vector[{visual_vector_dims}]",
    }


# Pydantic-style schemas for type hints
class TextChunkSchema:
    """Schema for text/paper chunks."""

    id: str
    content: str
    content_hash: str
    vector: list[float]
    source_file: str
    source_type: str
    start_line: int | None
    end_line: int | None
    start_char: int | None
    end_char: int | None
    parent_id: str | None
    title: str | None
    section_path: str | None
    citations: str | None
    token_count: int | None


class CodeChunkSchema:
    """Schema for code chunks."""

    id: str
    content: str
    content_hash: str
    vector: list[float]
    source_file: str
    source_type: str
    language: str | None
    start_line: int | None
    end_line: int | None
    start_char: int | None
    end_char: int | None
    parent_id: str | None
    symbol_name: str | None
    symbol_type: str | None
    imports: str | None
    token_count: int | None


class UnifiedChunkSchema:
    """Schema for unified chunks table."""

    id: str
    content: str
    content_hash: str
    vector: list[float]
    source_file: str
    source_type: str
    content_type: str
    language: str | None
    start_line: int | None
    end_line: int | None
    parent_id: str | None
    title: str | None
    section_path: str | None
    symbol_name: str | None
    symbol_type: str | None
    metadata_json: str | None
    token_count: int | None


class ImageChunkSchema:
    """Schema for image chunks table.

    Image chunks have dual embeddings:
    - text_vector: From VLM description (text search)
    - visual_vector: From CLIP/SigLIP (visual similarity)
    """

    id: str
    figure_id: int
    caption: str
    vlm_description: str
    classification: str
    page: int
    image_path: str
    source_paper: str
    text_vector: list[float]
    visual_vector: list[float]


def get_metadata_schema() -> dict:
    """Get schema for database metadata table.

    Stores key-value pairs for database configuration and portability.
    Keys include:
    - input_root: Original input directory (for path reconstruction)
    - created_at: Database creation timestamp
    - processor_version: Version of processor used

    Returns:
        Schema dictionary for table creation
    """
    return {
        "key": "string",
        "value": "string",
    }


class MetadataSchema:
    """Schema for database metadata table."""

    key: str
    value: str
