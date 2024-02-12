# /tests/unit/test_printing_repo.py

from datetime import datetime
from uuid import uuid4, UUID

import pytest

from app.models.document import Document
from app.repositories.local_document_repo import DocumentRepo

document_test_repo = DocumentRepo()


def test_empty_list() -> None:
    assert document_test_repo.get_document() == []


def test_add_first_document() -> None:
    document = Document(doc_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                        ord_id=uuid4(),
                        type='test_doc_type_1',
                        create_date=datetime.now(),
                        doc='test_doc_doc_1',
                        customer_info='test_customer_info_0')
    assert document_test_repo.create_document(document) == document


def test_add_first_document_repeat() -> None:
    document = Document(doc_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                        ord_id=uuid4(),
                        type='test_doc_type_1',
                        create_date=datetime.now(),
                        doc='test_doc_doc_1',
                        customer_info='test_customer_info_0')
    # document_test_repo.create_document(document)
    with pytest.raises(KeyError):
        document_test_repo.create_document(document)


def test_get_document_by_id() -> None:
    document = Document(doc_id=uuid4(),
                        ord_id=uuid4(),
                        type='test_doc_type_1',
                        create_date=datetime.now(),
                        doc='test_doc_doc_1',
                        customer_info='test_customer_info_0')
    document_test_repo.create_document(document)
    assert document_test_repo.get_document_by_id(document.doc_id) == document


def test_get_document_by_id_error() -> None:
    with pytest.raises(KeyError):
        document_test_repo.get_document_by_id(uuid4())
