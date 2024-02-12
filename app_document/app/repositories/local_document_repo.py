from typing import Optional
from uuid import UUID

from app.models.document import Document

# documents: list[Document] = [
#     Document(doc_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'), ord_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
#              type='test_doc_type_1', create_date=datetime.datetime.now(), doc='test_doc_doc_1',
#              customer_info='test_customer_info_0'),
#     Document(doc_id=UUID('45309954-8e3c-4635-8066-b342f634252c'), ord_id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
#              type='test_doc_type_2', create_date=datetime.datetime.now(), doc='test_doc_doc_2',
#              customer_info='test_customer_info_1'),
# ]

documents = []


class DocumentRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            documents.clear()

    def get_document(self) -> list[Document]:
        return documents

    # def get_doc_by_id(self, id: UUID) -> Document:
    #     for d in documents:
    #         if d.id == id:
    #             return d
    #
    #     raise KeyError

    def get_document_by_id(self, id: UUID) -> Document:
        for d in documents:
            if d.doc_id == id:
                return d

        raise KeyError

    def create_document(self, doc: Document) -> Document:
        if len([d for d in documents if d.doc_id == doc.doc_id]) > 0:
            raise KeyError

        documents.append(doc)
        return doc

    def delete_doc(self, id: UUID) -> Optional[Document]:
        for i, document in enumerate(documents):
            if document.doc_id == id:
                deleted_document = documents.pop(i)
                return deleted_document

        return None


