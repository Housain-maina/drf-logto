import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def test_client() -> APIClient:
    return APIClient()
