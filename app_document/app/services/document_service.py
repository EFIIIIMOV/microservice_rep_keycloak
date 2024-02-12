# 1. Поменять int на UUID в функциях

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import Depends

from app.models.document import Document
from app.repositories.db_document_repo import DocumentRepo


#from app.repositories.local_document_repo import DocumentRepo


# from app.repositories.local_deliveryman_repo import DeliverymenRepo


class DocumentService():
    order_repo: DocumentRepo

    # deliveryman_repo: DeliverymenRepo

    def __init__(self, document_repo: DocumentRepo = Depends(DocumentRepo)) -> None:
        self.document_repo = document_repo
        # self.deliveryman_repo = DeliverymenRepo()

    def get_document(self) -> list[Document]:
        return self.document_repo.get_document()

    def create_document(self, ord_id: UUID, type: str, doc: str, customer_info: str) -> Document:
        document = Document(doc_id=uuid4(), ord_id=ord_id, type=type, create_date=datetime.now(),
                            doc=doc, customer_info=customer_info)

        return self.document_repo.create_document(document)

    def delete_document(self, doc_id: UUID) -> None:
        return self.document_repo.delete_doc(doc_id)
