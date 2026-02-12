import pytest
from playwright.sync_api import Page, expect
from src.gui import InsurancePage

@pytest.fixture
def insurance_page(page: Page):
    return InsurancePage(page)


def test_hoff_title(insurance_page, page: Page):
    insurance_page.navigate()

    expect(page).to_have_title("Hoff's Insurance app")

# Fill Form test
@pytest.mark.parametrize("apartment_size, adults,  kids, coverage, expected_monthly", [
    (26, 1, 0, "100%", 110),
    (99, 2, 2, "50%", 117.5),
    pytest.param(167, 4, 3, "25%", 100, marks=pytest.mark.xfail(reason="Known bug in pricing logic")),
    pytest.param(50, 1, 1, "100%", 130, marks=pytest.mark.xfail(reason="Known bug in pricing logic")),
    pytest.param(150, 3, 2, "50%", 122.5, marks=pytest.mark.xfail(reason="Known bug in pricing logic"))
])
def test_fill_form(insurance_page, apartment_size, adults, kids, coverage, expected_monthly):
    insurance_page.navigate()   
    
    fname, lname, address, monthly_text = insurance_page.fill_form(apartment_size, adults, kids, coverage)

    expect(insurance_page.page.locator("#inputName")).to_have_value(fname)
    expect(insurance_page.page.locator("#inputSurname")).to_have_value(lname)
    expect(insurance_page.page.locator("#inputAddress")).to_have_value(address)

    expect(insurance_page.page.locator("#exampleModal")).to_be_visible()
    expect(insurance_page.page.locator("#monthly")).to_be_visible()
    expect(insurance_page.page.locator("#yearly")).to_be_visible()

    assert float(monthly_text) == expected_monthly


@pytest.mark.parametrize("apartment_size, adults,  kids, coverage", [
    (-100, 1, 0, "100%"),
    (99, -2, 2, "50%"),
    (167, 4, -3, "25%"), 
    (-50, -1, -1, "100%"), 
    (150, 3, 2, "50%"),
])
def test_fill_form_negative(insurance_page, apartment_size, adults, kids, coverage):
    insurance_page.navigate()   
    
    fname, lname, address, monthly_text = insurance_page.fill_form(apartment_size, adults, kids, coverage)

    expect(insurance_page.page.locator("#inputName")).to_have_value(fname)
    expect(insurance_page.page.locator("#inputSurname")).to_have_value(lname)
    expect(insurance_page.page.locator("#inputAddress")).to_have_value(address)

    expect(insurance_page.page.locator("#exampleModal")).to_be_visible()
    expect(insurance_page.page.locator("#monthly")).to_be_visible()
    expect(insurance_page.page.locator("#yearly")).to_be_visible()

# Testar att alla fält är synliga vid sidladdning
def test_all_form_fields_visible(insurance_page):
    insurance_page.navigate()
    expect(insurance_page.page.locator("#inputName")).to_be_visible()
    expect(insurance_page.page.locator("#inputSurname")).to_be_visible()
    expect(insurance_page.page.locator("#inputAddress")).to_be_visible()
    expect(insurance_page.page.locator("#inputSize")).to_be_visible()
    expect(insurance_page.page.locator("#inputAdults")).to_be_visible()
    expect(insurance_page.page.locator("#inputKids")).to_be_visible()
    expect(insurance_page.page.locator("#inputCoverage")).to_be_visible()
    expect(insurance_page.page.locator("#calcPriceBtn")).to_be_visible()

@pytest.mark.parametrize("coverage", ["100%", "50%", "25%"])
def test_coverage_options(insurance_page, coverage):
    insurance_page.navigate()
    
    fname, lname, address, monthly_text = insurance_page.fill_form(
        apartment_size=50, 
        adults=2, 
        kids=1, 
        coverage=coverage)

    # Verifiera valt coverage
    selected = insurance_page.page.locator("#inputCoverage").input_value()
    assert selected == coverage

    #Verifiera att modal visas och pris är större än 0
    expect(insurance_page.page.locator("#exampleModal")).to_be_visible()
    assert float(monthly_text) > 0