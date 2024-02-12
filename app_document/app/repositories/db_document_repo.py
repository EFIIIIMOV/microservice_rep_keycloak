import traceback
from uuid import UUID

from sqlalchemy.orm import Session

from app.database import get_db_doc
from app.models.document import Document
from app.schemas.document import Document as DBDocument


class DocumentRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db_doc())

    def _map_to_model(self, document: DBDocument) -> Document:
        result = Document.from_orm(document)

        return result

    def _map_to_schema(self, document: Document) -> DBDocument:
        data = dict(document)
        result = DBDocument(**data)

        return result

    def get_document(self) -> list[Document]:
        documents = []
        for d in self.db.query(DBDocument).all():
            documents.append(self._map_to_model(d))

        return documents

    def get_document_by_id(self, id: UUID) -> Document:
        document = self.db \
            .query(DBDocument) \
            .filter(DBDocument.doc_id == id) \
            .first()

        if document == None:
            raise KeyError
        return self._map_to_model(document)

    def create_document(self, document: Document) -> Document:
        try:
            db_document = self._map_to_schema(document)
            self.db.add(db_document)
            self.db.commit()
            return self._map_to_model(db_document)
        except:
            traceback.print_exc()
            raise KeyError

    def delete_all_document(self) -> None:
        try:
            # Delete all orders from the database
            self.db.query(DBDocument).delete()
            self.db.commit()
        except Exception as e:
            print(f"An error occurred while deleting all document: {e}")
            self.db.rollback()
            raise

    def delete_document_by_id(self, id: UUID) -> Document:
        try:
            # Find the order by its ord_id
            document = self.db.query(DBDocument).filter(DBDocument.doc_id == id).one()

            # If the order is found, map it to the model and commit the deletion
            if document:
                deleted_document = self._map_to_model(document)
                self.db.delete(document)
                self.db.commit()
                return deleted_document
            else:
                # Handle the case where no order is found
                raise ValueError(f"No order found with ord_id {id}")
        except Exception as e:
            # Rollback any changes if there's an error
            self.db.rollback()
            # Re-raise the exception so it can be handled elsewhere
            raise e
