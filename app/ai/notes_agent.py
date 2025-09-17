from dataclasses import dataclass
from textwrap import dedent

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.notes import create as create_note_dao
from app.services.ollama import find_relevant_notes_by_cosine


class Answer(BaseModel):
    answer: str


class CreatedNote(BaseModel):
    note_id: int


@dataclass
class DBDeps:
    session: AsyncSession


model = OpenAIChatModel(
    "gpt-4.1-mini",
    provider=OpenAIProvider(api_key=""),
)

agent = Agent(
    model=model,
    deps_type=DBDeps,
    instructions=dedent("""
        You manage a personal notes knowledge base.

        Behavior:
        - If the user's message is a QUESTION (e.g., asks "what, how, why", ends with '?'):
          1) Call the `search` tool with the query to retrieve relevant notes.
          2) Read that context and answer concisely and helpfully using ONLY that context.
          3) Return an `Answer` with the final text.

        - If the user asks to create/save a note OR just describes their day:
          1) Extract a short, meaningful `title` (<=80 chars) and the full `content`.
          2) Call the `create_note` tool once.
          3) Immediately return a `CreatedNote` with the new note_id. Do NOT add extra prose.

        Tie-breakers:
        - If both could apply, prefer CREATE only when they clearly asked to save; otherwise SEARCH.

        Style:
        - Keep answers short and to the point.
    """),
    output_type=[Answer, CreatedNote],
)


@agent.tool
async def search(ctx: RunContext[DBDeps], query: str) -> str:
    """
    Retrieve relevant notes for RAG.
    Returns a plain text context the model will read to answer.
    """
    rows = await find_relevant_notes_by_cosine(ctx.deps.session, query)
    chunks: list[str] = []

    for r in rows:
        chunks.append(f"[{r.id}] {r.title}\n{r.content}")

    return "\n\n---\n\n".join(chunks)


@agent.tool
async def create_note(ctx: RunContext[DBDeps], title: str, content: str) -> int:
    """
    Create a note and return its id.
    """
    note = await create_note_dao(session=ctx.deps.session, title=title, content=content)

    return note.id
