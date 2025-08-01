import os
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chainlit.logger import logger
from docx import Document
from langchain.indexes import aindex
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .envs import RESUMES_PATH


def save_to_latest(latest: Path):
    """Move current latest resume to timestamped directory, then save the new latest resume."""
    dashTime = datetime.now(UTC).strftime("%Y-%m-%d-%H-%M-%S")
    if not os.path.exists(RESUMES_PATH / dashTime):
        (RESUMES_PATH / dashTime).mkdir(parents=True)
    if not os.path.exists(RESUMES_PATH / "latest"):
        (RESUMES_PATH / "latest").mkdir(parents=True)

    for item in (RESUMES_PATH / "latest").iterdir():
        if item.is_file():
            shutil.move(str(item.resolve()), str((RESUMES_PATH / dashTime).resolve()))
            break

    shutil.move(str(latest.resolve()), str((RESUMES_PATH / "latest").resolve()))


async def process_docx(
    docx_path: Path,
    recordmanager: Any,
    vectordb: Any,
    *,
    chunk_size: int = 50,
    chunk_overlap: int = 5,
):
    """
    Process the uploaded DOCX file and extract its content.
    Put chunks into vectordb.
    """
    doc = Document(str(docx_path))
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    chunks = text_splitter.split_documents(doc)

    index_result = await aindex(
        chunks,
        recordmanager,
        vectordb,
        cleanup="incremental",
        source_id_key="source",
    )
    logger.info(f"Indexing stats: {index_result}")
