import os
from functools import partial
from operator import itemgetter
from pathlib import Path
from typing import Dict, Optional

import chainlit as cl
from chainlit.logger import logger
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector

from resume import no_resume_exists
from utils.blob import process_docx, save_to_latest
from utils.db import LocalRecordManager, _cleanup, a_pgvector_engine
from utils.envs import RESUMES_PATH, SUGGESTIONS_PATH

embeddings_model = OpenAIEmbeddings()
model = ChatOpenAI(model_name="gpt-4o-mini", streaming=True)


@cl.on_chat_start
async def on_chat_start():
    """Prepare for chat."""
    # resource setup: pgvector and record manager
    vectordb = PGVector(
        embeddings_model,
        collection_name=cl.user_session.get("id"),
        connection=a_pgvector_engine,
        use_jsonb=True,
    )
    await vectordb.__apost_init__()
    cl.user_session.set("vectordb", vectordb)

    recordmanager = LocalRecordManager(cl.user_session.get("id"))
    cl.user_session.set("recordmanager", recordmanager)

    # prepare for latest resume
    if no_resume_exists():
        latestResume = await cl.AskFileMessage(
            content="Please upload your latest resume to begin!",
            accept={"text/plain": [".docx"]},
        ).send()

        if len(latestResume) > 1:
            await cl.Message(content="Please upload only one resume at a time.").send()
            return

        latestResume = Path(latestResume[0].path)
        save_to_latest(latestResume)
    else:
        latestPath = RESUMES_PATH / "latest"
        for item in latestPath.iterdir():
            if item.is_file():
                latestResume = item.resolve()
                break

    process_docx(latestResume)


@cl.on_settings_update
async def setup_agent(settings):
    logger.info("on_settings_update", settings)


@cl.on_message
async def on_message(message: cl.Message):
    """Logic for handling the user's message.

    Args:
        message (cl.Message): Response to the user's message.
    """

    print("on_message", message)


@cl.on_chat_end
async def on_chat_end():
    """Delete the index and vectors."""
    print("on_chat_end")
    vectordb = cl.user_session.get("vectordb")
    recordmanager = cl.user_session.get("recordmanager")
    await _cleanup(cl.user_session.get("id"), vectordb, recordmanager)
