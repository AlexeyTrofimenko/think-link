from dataclasses import dataclass
from textwrap import dedent

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.notes import update


class Answer(BaseModel):
    answer: str


class UpdatedNote(BaseModel):
    note_id: int


@dataclass
class NoteDeps:
    session: AsyncSession
    note_id: int


model = OpenAIChatModel(
    "gpt-4.1-mini",
    provider=OpenAIProvider(api_key=""),
)

agent = Agent(
    model=model,
    deps_type=NoteDeps,
    tools=[
        duckduckgo_search_tool(),
    ],
    instructions=dedent("""
    You manage a personal note.

    Behavior:
    - If the user's message is a request to CHANGE the note (title or content):
      1) Determine the intended new_title and/or new_content.
      2) Call the `change_note` tool exactly once with the computed fields (omit fields that should not change).
      3) Immediately return an `UpdatedNote` with the note_id. Do NOT add extra prose.

    - If the user wants to EXTEND the note using the web:
      1) Call `duckduckgo_search` with a focused query to gather context.
      2) Compose a concise, factually grounded addition (1–3 short paragraphs).
      3) Call `change_note` with new_content containing the original content plus your addition.
      4) Immediately return an `UpdatedNote` with the note_id. Do NOT add extra prose.

    - If the user's message is a QUESTION about the current note (or your steps):
      1) Answer concisely and helpfully using the provided note content and any results you fetched.
      2) Return an `Answer` with the final text.

    Tie-breakers:
    - Prefer CHANGE only when clearly asked to modify the note; otherwise answer questions as `Answer`.

    Style:
    - Keep answers short and to the point.
    """),  # noqa: E501
    output_type=[Answer, UpdatedNote],
)


@agent.tool
async def change_note(
    ctx: RunContext[NoteDeps], new_title: str | None = None, new_content: str | None = None
) -> int:
    """
    Update a current note and return its id.
    """

    note = await update(
        session=ctx.deps.session,
        note_id=ctx.deps.note_id,
        title=new_title,
        content=new_content,
    )

    if note:
        return note.id
    return 0
