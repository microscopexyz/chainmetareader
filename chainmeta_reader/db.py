# Copyright 2023 The chainmetareader Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from typing import Generator, Iterable

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from unsync import unsync

from chainmeta_reader.logger import logger
from chainmeta_reader.metadata import ChainmetaItem, Tag

# Define the database connection
Engine = None
Base = declarative_base()


# Define the table using declarative ORM
class ChainmetaTable(Base):
    __tablename__ = "chainmeta"

    id = Column(Integer, primary_key=True)
    chain = Column(String(64), nullable=False)
    address = Column(String(256), nullable=False)
    namespace = Column(String(64), nullable=False)
    scope = Column(String(64), nullable=False)
    tag = Column(String(64), nullable=False)
    source = Column(String(64), nullable=False)
    submitted_by = Column(String(64), nullable=False)
    submitted_on = Column(DateTime(), nullable=False)


def init_db(connection_string: str) -> callable:
    global Engine

    # Initialize the database connection
    Engine = create_engine(connection_string)

    # Create a sessionmaker object to interact with the database
    session_factory = sessionmaker(bind=Engine)
    return scoped_session(session_factory)


@unsync
def add_chainmeta_single_batch(
    session_maker: callable, items: Iterable[ChainmetaItem]
) -> int:
    """Add a batch of chain metadata to database."""
    logger.info(f"Adding {len(items)} items to database")
    with session_maker() as session:
        total = 0
        for item in items:
            meta_item = ChainmetaTable(
                chain=item.chain.name,
                address=item.address,
                namespace=item.tag.namespace,
                scope=item.tag.scope,
                tag=item.tag.name,
                source=item.source,
                submitted_by=item.submitted_by,
                submitted_on=datetime.now(),
            )

            if (
                session.query(ChainmetaTable)
                .filter_by(
                    chain=item.chain.name,
                    address=item.address,
                    namespace=item.tag.namespace,
                    scope=item.tag.scope,
                    tag=item.tag.name,
                    source=item.source,
                    submitted_by=item.submitted_by,
                )
                .first()
                is None
            ):
                total += 1
                session.add(meta_item)
        session.commit()
        return total


def add_chainmeta(
    session_maker: callable,
    items: Iterable[ChainmetaItem],
    batch_size: int = 50,
    max_concurrency: int = 10,
) -> int:
    """Add chain metadata to database."""
    total, batch, tasks = 0, [], []
    for item in items:
        batch += [item]
        if len(batch) >= batch_size:
            tasks += [add_chainmeta_single_batch(session_maker, batch)]
            batch = []
            if len(tasks) >= max_concurrency:
                total += sum(task.result() for task in tasks)
                tasks = []

    if batch:
        tasks += [add_chainmeta_single_batch(session_maker, batch)]
    if tasks:
        total += sum(task.result() for task in tasks)

    return total


def search_chainmeta(
    session_maker: callable, *, filter: dict = None
) -> Generator[ChainmetaItem, None, None]:
    """Search chain metadata from database."""

    def _apply_filter(query: object, filter: dict) -> object:
        """Apply filter to query."""

        if not filter:
            return query

        if filter.keys() == set(["chain"]):
            return query.filter_by(chain=filter["chain"])

        if filter.keys() == set(["chain", "address"]):
            return query.filter_by(chain=filter["chain"], address=filter["address"])

        if filter.keys() == set(["chain", "namespace", "scope", "tag"]):
            return query.filter_by(
                chain=filter["chain"],
                namespace=filter["namespace"],
                scope=filter["scope"],
                tag=filter["tag"],
            )

        if filter.keys() == set(["submitted_by"]):
            return query.filter_by(submitted_by=filter["submitted_by"])

        logger.warning(f"Unsupported filter: {filter}")
        return query

    session = session_maker()
    page_size = 100
    page_num = 1
    is_empty = True
    while True:
        query = _apply_filter(session.query(ChainmetaTable), filter)
        results = (
            query.order_by(ChainmetaTable.address)
            .limit(page_size)
            .offset((page_num - 1) * page_size)
            .all()
        )
        if not results:
            break
        for r in results:
            is_empty = False
            yield ChainmetaItem(
                r.chain,
                r.address,
                Tag(r.namespace, r.scope, r.tag),
                r.source,
                r.submitted_by,
                r.submitted_on,
            )
        page_num += 1
    if is_empty:
        return
    session.close()
