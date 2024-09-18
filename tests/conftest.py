import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def test_client() -> APIClient:
    return APIClient()
