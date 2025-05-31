import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_healthcheck(client):
    response = client.get("/")
    assert response.status_code == 200
