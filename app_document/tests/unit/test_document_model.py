# /tests/unit/test_printing_model.py

from datetime import datetime
from uuid import uuid4, UUID


import pytest
from pydantic import ValidationError

from app.models.document import Document

doc_id: UUID
ord_id: UUID
type: str
customer_info: str
create_date: datetime
doc: str


def test_document_creation():
    doc_id = uuid4()
    ord_id = uuid4()
    type = 'test_doc_type_1'
    create_date = datetime.now()
    doc = 'test_doc_doc_1'
    customer_info = 'test_customer_info_0'

    document = Document(doc_id=doc_id, ord_id=ord_id, type=type, create_date=create_date, doc=doc,
                        customer_info=customer_info)

    assert dict(document) == {'doc_id': doc_id, 'ord_id': ord_id, 'type': type,
                              'create_date': create_date, 'doc': doc,
                              'customer_info': customer_info}


def test_document_date_required():
    with pytest.raises(ValidationError):
        Document(doc_id=uuid4(),
                 ord_id=uuid4(),
                 type='test_doc_type_1',
                 doc='test_doc_doc_1',
                 customer_info='test_customer_info_0')


def test_document_ord_id_required():
    with pytest.raises(ValidationError):
        Document(doc_id=uuid4(),
                 type='test_doc_type_1',
                 create_date=datetime.now(),
                 doc='test_doc_doc_1',
                 customer_info='test_customer_info_0')
