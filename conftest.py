from graphene.test import Client
import pytest

from unsplash import api
from unsplash.schema import schema


@pytest.fixture
def client():
    return Client(schema=schema)


@pytest.fixture
def hmm():
    pass


