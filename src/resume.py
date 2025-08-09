import os
from pathlib import Path
from typing import Any

from chainlit.logger import logger
from docx import Document
from langchain.indexes import aindex
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.envs import RESUMES_PATH


def no_resume_exists():
    """
    Check if a resume has been uploaded by the user.
    Returns True if no resume exists, otherwise False.
    """
    if not os.path.exists(RESUMES_PATH / "latest"):
        (RESUMES_PATH / "latest").mkdir(parents=True)
    for item in RESUMES_PATH.iterdir():
        if item.is_dir() and item.name == "latest":
            return True
    return False


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
