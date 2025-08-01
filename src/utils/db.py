import asyncio
import os

from chainlit.logger import logger
from langchain.indexes import SQLRecordManager, aindex
from langchain_postgres.vectorstores import PGVector
from sqlalchemy.ext.asyncio import create_async_engine

a_pgvector_engine = create_async_engine(os.getenv("PGVECTOR_CONNECTION_STRING"))
a_record_engine = create_async_engine(os.getenv("RECORDMANAGER_CONNECTION_STRING"))


class LocalRecordManager:
    """Singleton class for managing local record managers.

    Returns:
        SQLRecordmanager: return the instance of the SQLRecordManager.
    """

    _instance = dict()

    def __new__(cls, namespace: str) -> SQLRecordManager:
        if cls._instance.get(namespace, None) is None:
            sqlRecordManager = SQLRecordManager(namespace, engine=a_record_engine)
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:  # 'RuntimeError: There is no current event loop...'
                loop = None

            try:
                if loop and loop.is_running():
                    loop.run_until_complete(sqlRecordManager.acreate_schema())
                else:
                    asyncio.run(sqlRecordManager.acreate_schema())
            except Exception as e:
                # schema already exists, avoid crashing.
                logger.error(f"failed to create schema, schema exists.\n{e}")
            cls._instance[namespace] = sqlRecordManager

        return cls._instance[namespace]


async def _cleanup(
    uid: str, vectordb: PGVector, recordmanager: LocalRecordManager
) -> None:
    await aindex(
        [],
        recordmanager,
        vectordb,
        cleanup="full",
    )
    # files uploaded will be deleted after each session
