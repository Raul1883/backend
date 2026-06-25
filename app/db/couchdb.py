import base64
import zlib

import httpx
from fastapi import HTTPException
import urllib.parse
from app.config import config

COUCHDB_URL = config.COUCHDB_URL
COUCHDB_USER = config.COUCHDB_USER
COUCHDB_PASSWORD = config.COUCHDB_PASSWORD
DB_NAME = config.DB_NAME

class CouchDBClient:
    def __init__(self):
        self.client: httpx.AsyncClient | None = None

    def start(self):
        self.client = httpx.AsyncClient(
            base_url=COUCHDB_URL,
            auth=(COUCHDB_USER, COUCHDB_PASSWORD),
            timeout=10.0
        )

    async def stop(self):
        if self.client:
            await self.client.aclose()

    async def _get_raw_doc(self, doc_id: str) -> dict:
        """Внутренний метод для получения сырого документа по ID"""
        safe_doc_id = urllib.parse.quote(doc_id, safe="")
        response = await self.client.get(f"/{DB_NAME}/{safe_doc_id}")
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Документ '{doc_id}' не найден")
        
        response.raise_for_status()
        return response.json()

    async def get_document(self, doc_id: str) -> dict:
        if not self.client:
            raise RuntimeError("CouchDB client is not initialized")
        
        # 1. Получаем мета-документ заметки
        meta_doc = await self._get_raw_doc(doc_id)
        
        chunks_ids = meta_doc.get("children", [])
        if not chunks_ids:
            return {
                "id": meta_doc.get("_id"),
                "title": meta_doc.get("path", doc_id).split("/")[-1].replace(".md", ""),
                "content": "",
                "metadata": {}
            }
        
        # 2. Собираем текст из чанков напрямую
        full_content_parts = []
        for chunk_id in chunks_ids:
            chunk_doc = await self._get_raw_doc(chunk_id)
            
            # Поскольку данные хранятся в сыром виде, 
            # просто забираем строку из поля "data"
            raw_text = chunk_doc.get("data", "")
            if raw_text:
                full_content_parts.append(raw_text)

        # Склеиваем куски (если файл большой и разбился на несколько чанков)
        full_markdown = "".join(full_content_parts)

        return {
            "id": meta_doc.get("_id"),
            "title": meta_doc.get("path", doc_id).split("/")[-1].replace(".md", ""),
            "content": full_markdown,
            "metadata": {}
        }


    async def get_all_docs_ids(self) -> list[str]:
        if not self.client:
            raise RuntimeError("CouchDB client is not initialized")
            
        response = await self.client.get(f"/{DB_NAME}/_all_docs?include_docs=true")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Не удалось получить список страниц")
        
        rows = response.json().get("rows", [])
        
        clean_pages = []
        for row in rows:
            doc_id = row["id"]
            doc_body = row.get("doc", {})
            
            if (not doc_id.startswith("_") and 
                not doc_id.startswith("h:") and 
                not doc_body.get("deleted", False) and 
                not doc_body.get("_deleted", False)):
                clean_pages.append(doc_id)
                
        return clean_pages

couch_client = CouchDBClient()