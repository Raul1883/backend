from fastapi import APIRouter, Depends
from app.db.couchdb import CouchDBClient
from app.dependencies.database import get_db_client

# Создаем роутер с префиксом. Теперь все эндпоинты внутри будут начинаться с /api/wiki
router = APIRouter(prefix="/wiki", tags=["Wiki"])

@router.get("/{page_id:path}")
async def get_wiki_page(page_id: str, db: CouchDBClient = Depends(get_db_client)):
    doc = await db.get_document(page_id)
    
    # Твоя логика обработки специфики Live Sync
    markdown_content = doc.get("data", doc.get("content", ""))
    
    return {
        "id": doc.get("_id"),
        "title": doc.get("title", page_id),
        "content": markdown_content,
        "metadata": doc.get("frontmatter", {})
    }

@router.get("")
async def list_wiki_pages(db: CouchDBClient = Depends(get_db_client)):
    pages = await db.get_all_docs_ids()
    return {"pages": pages}