import pytest
import random
from src.api import PetstoreClient

@pytest.fixture
def api():
    return PetstoreClient()


#@pytest.mark.flaky(reruns=3, reruns_delay=1)
#@pytest.mark.parametrize("pet_id", [1, 2, 3])
#def test_get_pet_by_id(api, pet_id):
#    response = api.get_pet(pet_id)
#    data = response.json()
#    
#    assert response.status_code == 200
#    assert data["id"] == pet_id
#    assert "name" in data


#def test_get_pet_not_found(api):
#    response = api.get_pet(999999)
#    assert response.status_code == 404


def test_create_pet_with_client(api):  
    pet = {
        "id": random.randint(1, 1000),
        "name": "cat",
        "photoUrls": ["string"],
        "status": "available"
    }

    response = api.create_pet(pet)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == pet["id"]
    assert data["name"] == "cat"


@pytest.mark.parametrize("pet_data", [
    {
        "id": 93001,
        "name": "HelinDogUpdated",
        "status": "available"
    },
    {
        "id": 93002,
        "name": "HelinCatUpdated",
        "status": "sold"
    }
])
def test_update_pet(api, pet_data):
    """
    UPDATE (PUT) test för Petstore API
    """
    response = api.update_pet(pet_data)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == pet_data["id"]
    assert data["name"] == pet_data["name"]
    assert data["status"] == pet_data["status"]

@pytest.fixture
def created_pet(api):
    pet= {
        "id" : random.randint(10000, 99999),
        "name": "ToDelete",
        "status": "available",
        "photoUrls": ["string"]
    }

    response = api.create_pet(pet)
    assert response.status_code == 200
    return pet

def test_delete_pet_by_id(api, created_pet):

    pet_id = created_pet["id"]
    response = api.delete_pet(pet_id)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == str(pet_id)


@pytest.mark.parametrize("pet_id, pet_name", [
    (11111, "Dog1"),
    (22222, "Cat1"),
    (33333, "Bird1")
])
def test_delete_pet_parametrized(api, pet_id, pet_name):
    new_pet = {
        "id": pet_id,
        "name": pet_name,
        "status": "available",
        "photoUrls": ["string"]
    }
    
    create_response = api.create_pet(new_pet)
    assert create_response.status_code == 200
    
    # Radera pet
    response = api.delete_pet(pet_id)
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == str(pet_id)