# Importerar Page från Playwright för att kunna interagera med webbsidor
from playwright.sync_api import Page

from faker import Faker

class InsurancePage:
    def __init__(self, page: Page):
        # Sparar Playwrights page-objekt så vi kan använda det i klassen
        self.page = page
        
         # URL till försäkringssidan som ska testas
        self.url = "https://hoff.is/insurance"

    
    def navigate(self):
        #Navigerar till försäkringssidan.
        self.page.goto(self.url)

    def create_fake_data(self):
        """
        Skapar fejkad testdata (namn och adress) med svenska uppgifter.
        """
        fake = Faker('sv_SE')

        fname = fake.first_name()
        lname = fake.last_name()
        
        # Faker returnerar adress med radbrytning, ersätts med mellanslag
        address = fake.address().replace("\n", " ")

        return fname, lname, address


    def fill_form(self, apartment_size, adults, kids, coverage):
        """
        Fyller i försäkringsformuläret och beräknar priset.

        Parametrar:
        - apartment_size: storlek på bostaden
        - adults: antal vuxna
        - kids: antal barn
        - coverage: vald försäkringsnivå
        """
        
        # Hämtar fejkad testdata
        fname, lname, address = self.create_fake_data()

        # Fyller i formulärets fält
        self.page.locator("#inputName").fill(fname)
        self.page.locator("#inputSurname").fill(lname)
        self.page.locator("#inputAddress").fill(address)
        self.page.locator("#inputSize").fill(str(apartment_size))
        self.page.locator("#inputAdults").fill(str(adults))
        self.page.locator("#inputKids").fill(str(kids))
        
        # Väljer försäkringsnivå från dropdown
        self.page.locator("#inputCoverage").select_option(coverage)
        
        # Klickar på knappen för att räkna ut priset
        self.page.locator("#calcPriceBtn").click()

        # Hämtar texten för månadskostnaden efter beräkning
        monthly_text = self.page.locator("#monthly").inner_text()

        # Returnerar använd data + beräknat pris
        return fname, lname, address, monthly_text