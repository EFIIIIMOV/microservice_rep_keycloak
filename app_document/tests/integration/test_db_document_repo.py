# /tests/integration/app_repositories/test_db_delivery_repo.py

from datetime import datetime
from uuid import UUID, uuid4

import pytest

from app.models.document import Document
from app.repositories.db_document_repo import DocumentRepo


@pytest.fixture()
def document_repo() -> DocumentRepo:
    repo = DocumentRepo()
    return repo


@pytest.fixture(scope='session')
def document_id() -> UUID:
    return uuid4()


@pytest.fixture(scope='session')
def first_document() -> Document:
    return Document(doc_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                    ord_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                    type='test_doc_type_1', create_date=datetime.now(),
                    doc='test_doc_doc_1', customer_info='test_customer_info_0')


@pytest.fixture(scope='session')
def second_document() -> Document:
    return Document(doc_id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
                    ord_id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
                    type='test_doc_type_2', create_date=datetime.now(),
                    doc='test_doc_doc_2', customer_info='test_customer_info_1')


# def test_empty_list(document_repo: DocumentRepo) -> None:
#     document_repo.delete_all_document()
#     assert document_repo.get_document() == []


def test_add_first_document(first_document: Document, document_repo: DocumentRepo) -> None:
    assert document_repo.create_document(first_document) == first_document


def test_add_first_document_repeat(first_document: Document, document_repo: DocumentRepo) -> None:
    with pytest.raises(KeyError):
        document_repo.create_document(first_document)


def test_get_document_by_id(first_document: Document, document_repo: DocumentRepo) -> None:
    assert document_repo.get_document_by_id(first_document.doc_id) == first_document


def test_get_document_by_id_error(document_repo: DocumentRepo) -> None:
    with pytest.raises(KeyError):
        document_repo.get_document_by_id(uuid4())


def test_add_second_document(first_document: Document, second_document: Document, document_repo: DocumentRepo) -> None:
    assert document_repo.create_document(second_document) == second_document
    documents = []
    documents.append(document_repo.get_document_by_id(first_document.doc_id))
    documents.append(document_repo.get_document_by_id(second_document.doc_id))
    assert len(documents) == 2
    assert documents[0] == first_document
    assert documents[1] == second_document


def test_delete_created_order(first_document: Document, second_document: Document, document_repo: Document) -> None:
    assert document_repo.delete_document_by_id(first_document.doc_id) == first_document
    assert document_repo.delete_document_by_id(second_document.doc_id) == second_document
