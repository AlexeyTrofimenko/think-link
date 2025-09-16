import httpx
from pgvector.sqlalchemy import Vector
from sqlalchemy import bindparam, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import async_session
from app.db.models.note import Note
from app.schemas.rag import RAGSearchResultItem
from app.services.settings_ollama import ollama_settings


async def embed_text(text: str, ollama_url: str, ollama_embed_model: str) -> list[float]:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{ollama_url}/api/embeddings",
            json={"model": ollama_embed_model, "prompt": text},
        )
        r.raise_for_status()
        embeddings: list[float] = r.json()["embedding"]
        return embeddings


async def compute_note_embedding(note_id: int, content: str | None) -> None:
    if ollama_settings.OLLAMA_DISABLED or not ollama_settings.OLLAMA_URL or content is None:
        return
    vec = await embed_text(content, ollama_settings.OLLAMA_URL, ollama_settings.OLLAMA_EMBED_MODEL)

    async with async_session() as s:
        await s.execute(update(Note).where(Note.id == note_id).values(embedding=vec))
        await s.commit()


async def find_relevant_notes_by_cosine(
    session: AsyncSession,
    query_text: str,
    k: int = 5,
    max_distance: float | None = None,
) -> list[RAGSearchResultItem]:
    qvec = []
    if not ollama_settings.OLLAMA_DISABLED and ollama_settings.OLLAMA_URL:
        qvec = await embed_text(
            query_text, ollama_settings.OLLAMA_URL, ollama_settings.OLLAMA_EMBED_MODEL
        )

    qparam: Vector = bindparam("qvec", value=qvec, type_=Vector(len(qvec)))

    dist = Note.embedding.cosine_distance(qparam).label("distance")

    stmt = select(Note.id, dist).where(Note.embedding.is_not(None)).order_by(dist).limit(k)

    res = await session.execute(stmt)
    rows = [RAGSearchResultItem(id=r.id, distance=float(r.distance)) for r in res.all()]

    if max_distance is not None:
        rows = [item for item in rows if item.distance <= max_distance]

    return rows
