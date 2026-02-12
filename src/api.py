import requests

# Klient för att interagera med Petstore API (CRUD-operationer)
class PetstoreClient:
    def __init__(self): # Initierar klienten med bas-URL och API-nyckel
        self.base_url = "https://petstore.swagger.io/v2"

    def create_pet(self, pet_data):
        url = f"{self.base_url}/pet"
        response = requests.post(url, json=pet_data) # Skickar POST-förfrågan
        return response






    def get_pet(self, pet_id):
        url = f"{self.base_url}/pet/{pet_id}"
        response = requests.get(url) # Get hämtar/läser
        return response
    
    
    def update_pet(self, pet_data):
        url = f"{self.base_url}/pet"
        response = requests.put(url, json=pet_data) # PUT uppdaterar en befintlig resurs
        return response
    

    def delete_pet(self, pet_id):
        url = f"{self.base_url}/pet/{pet_id}"
        response = requests.delete(url) # DELETE tar bort en resurs
        return response