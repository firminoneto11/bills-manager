from contextlib import asynccontextmanager
from gc import collect
from typing import TYPE_CHECKING, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
    from sqlalchemy.orm import DeclarativeBase


class DBConnectionHandler:
    _connection_string: str
    _engine: Optional["AsyncEngine"] = None
    _make_session: Optional[async_sessionmaker["AsyncSession"]] = None
    _active_sessions: Optional[set["AsyncSession"]] = None
    _is_connected: bool = False

    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def _validate_connection(self):
        if not self._is_connected:
            raise ConnectionError("This instance is not connected to the database yet")

    async def _test_connection(self):
        error, self._is_connected = None, True
        try:
            async with self.begin_session() as session:
                await session.execute(text("SELECT 1;"))
        except Exception as exc:
            error = exc
        finally:
            self._is_connected = False

        if error:
            await self.disconnect()
            raise ConnectionError("Failed to connect to the database.") from error

    def _reset(self):
        self._engine = None
        self._make_session = None
        self._active_sessions = None
        self._is_connected = False
        collect()

    @property
    def using_sqlite(self):
        return self._connection_string.startswith("sqlite")

    @property
    def engine(self):
        if self._engine is None:
            raise ValueError("'_engine' is None. Can not proceed.")
        return self._engine

    @property
    def make_session(self):
        if self._make_session is None:
            raise ValueError("'_make_session' is None. Can not proceed.")
        return self._make_session

    @property
    def active_sessions(self):
        if self._active_sessions is None:
            self._active_sessions = set()
        return self._active_sessions

    async def connect(
        self, echo_sql: bool = False, pool_size: int = 5, max_overflow: int = 10
    ):
        if self._is_connected:
            return

        kws = dict()
        if self.using_sqlite:
            kws["connect_args"] = {"check_same_thread": False}
        else:
            kws["pool_size"] = pool_size
            kws["max_overflow"] = max_overflow

        self._engine = create_async_engine(
            url=self._connection_string, echo=echo_sql, **kws
        )

        self._make_session = async_sessionmaker(
            self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

        await self._test_connection()

        self._is_connected = True

    async def disconnect(self):
        [await ses.close() for ses in self.active_sessions]

        try:
            await self.engine.dispose()
        except ValueError:
            pass

        self._reset()

    async def migrate(self, base_model: "DeclarativeBase", drop: bool = False):
        self._validate_connection()

        async with self.engine.begin() as conn:
            if drop:
                await conn.run_sync(base_model.metadata.drop_all)
            await conn.run_sync(base_model.metadata.create_all)

            # NOTE: This option has to be enabled in order to use foreign key
            # constraints for sqlite. Check:
            # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
            if self.using_sqlite:
                await conn.execute(text("PRAGMA foreign_keys=ON"))

    @asynccontextmanager
    async def begin_session(self):
        self._validate_connection()
        self.active_sessions.add(session := self.make_session())
        async with session:
            try:
                yield session
            except Exception as exc:
                await session.rollback()
                raise exc
            finally:
                self.active_sessions.remove(session)

    async def ping(self):
        try:
            async with self.begin_session() as session:
                await session.execute(text("SELECT 1;"))
        except Exception as exc:
            raise ConnectionError("Failed to connect to the database.") from exc
