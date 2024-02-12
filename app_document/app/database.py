from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

# from app.settings import settings

# engine_ord = create_engine(settings.postgres_url_ord, echo=True)
engine_doc = create_engine(settings.postgres_url_doc, echo=True)
# SessionLocalOrd = sessionmaker(autocommit=False, autoflush=False, bind=engine_ord)
SessionLocalDoc = sessionmaker(autocommit=False, autoflush=False, bind=engine_doc)


def get_db_ord():
    pass
    # db_ord = SessionLocalOrd()
    # try:
    #     yield db_ord
    # finally:
    #     db_ord.close()


def get_db_doc():
    db_doc = SessionLocalDoc()
    try:
        yield db_doc
    finally:
        db_doc.close()
