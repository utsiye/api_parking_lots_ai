from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ARRAY, Float, Boolean, ForeignKey, Date
from sqlalchemy.dialects.postgresql import JSON

from app.misc.logger import logger
from app.settings.config import load_config

db = Gino()
config = load_config()
db_config = config.db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, nullable=False)
    ...



    def __repr__(self):
        return f"User(id={self.id})"


async def create_db():
    logger.info("Connecting to database")
    await db.set_bind(f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}/{db_config.database}")
    # noinspection PyTypeHints
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()
    await db.gino.create_all()
