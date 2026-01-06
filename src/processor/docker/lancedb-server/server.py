"""LanceDB REST API Server.

A simple FastAPI server that wraps LanceDB for remote access.
Supports vector search, hybrid search, and table listing.
"""

import os

import lancedb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="LanceDB Server",
    description="REST API for LanceDB vector database",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DB_PATH = os.environ.get("LANCEDB_PATH", "/data")
db: lancedb.DBConnection | None = None


def get_db() -> lancedb.DBConnection:
    """Get or create database connection."""
    global db
    if db is None:
        db = lancedb.connect(DB_PATH)
    return db


class SearchRequest(BaseModel):
    """Search request body."""
    query_vector: list[float]
    limit: int = 10
    filter: str | None = None


class HybridSearchRequest(BaseModel):
    """Hybrid search request body."""
    query_vector: list[float]
    query_text: str
    limit: int = 10
    filter: str | None = None


class TextSearchRequest(BaseModel):
    """Full-text search request body."""
    query_text: str
    limit: int = 10


@app.get("/")
async def root():
    """Health check and info."""
    return {
        "service": "LanceDB Server",
        "database": DB_PATH,
        "status": "healthy",
    }


@app.get("/healthz")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/tables")
async def list_tables():
    """List all tables in the database."""
    try:
        connection = get_db()
        tables = connection.table_names()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/tables/{table_name}")
async def table_info(table_name: str):
    """Get table information."""
    try:
        connection = get_db()
        if table_name not in connection.table_names():
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        table = connection.open_table(table_name)
        return {
            "name": table_name,
            "row_count": table.count_rows(),
            "schema": str(table.schema),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tables/{table_name}/schema")
async def table_schema(table_name: str):
    """Get table schema."""
    try:
        connection = get_db()
        if table_name not in connection.table_names():
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        table = connection.open_table(table_name)
        schema = table.schema
        columns = []
        for field in schema:
            columns.append({
                "name": field.name,
                "type": str(field.type),
            })
        return {"columns": columns}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tables/{table_name}/search")
async def vector_search(table_name: str, request: SearchRequest):
    """Perform vector search on a table."""
    try:
        connection = get_db()
        if table_name not in connection.table_names():
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        table = connection.open_table(table_name)

        query = table.search(request.query_vector).limit(request.limit)
        if request.filter:
            query = query.where(request.filter)

        results = query.to_list()

        return {
            "results": results,
            "count": len(results),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tables/{table_name}/search/hybrid")
async def hybrid_search(table_name: str, request: HybridSearchRequest):
    """Perform hybrid (vector + FTS) search on a table."""
    try:
        connection = get_db()
        if table_name not in connection.table_names():
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        table = connection.open_table(table_name)

        query = (
            table.search(query_type="hybrid")
            .vector(request.query_vector)
            .text(request.query_text)
            .limit(request.limit)
        )
        if request.filter:
            query = query.where(request.filter)

        results = query.to_list()

        return {
            "results": results,
            "count": len(results),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tables/{table_name}/search/text")
async def text_search(table_name: str, request: TextSearchRequest):
    """Perform full-text search on a table."""
    try:
        connection = get_db()
        if table_name not in connection.table_names():
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        table = connection.open_table(table_name)

        results = (
            table.search(request.query_text, query_type="fts")
            .limit(request.limit)
            .to_list()
        )

        return {
            "results": results,
            "count": len(results),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tables/{table_name}/rows")
async def get_rows(table_name: str, limit: int = 50, offset: int = 0):
    """Get rows from a table (paginated)."""
    try:
        connection = get_db()
        if table_name not in connection.table_names():
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        table = connection.open_table(table_name)

        # Use Arrow for efficient pagination
        arrow_table = table.to_arrow()
        total = arrow_table.num_rows

        # Slice for pagination
        sliced = arrow_table.slice(offset, limit)
        rows = sliced.to_pylist()

        return {
            "rows": rows,
            "total": total,
            "offset": offset,
            "limit": limit,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metadata")
async def get_metadata():
    """Get database metadata."""
    try:
        connection = get_db()

        if "_metadata" not in connection.table_names():
            return {"metadata": {}}

        table = connection.open_table("_metadata")
        rows = table.to_pandas()
        metadata = dict(zip(rows["key"], rows["value"], strict=False))

        return {"metadata": metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
