import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture(scope="function")
def setup():
    # ChromeDriver kurulumunu yap
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    yield driver
    driver.quit()

def test_amazon_login_and_search(setup):
    driver = setup
    email = "qualityasurance9@gmail.com"
    password = "Test1234!"

    # Amazon ana sayfasına git
    driver.get("https://www.amazon.com")

    # Oturum açma sayfasına git
    driver.find_element(By.ID, "nav-link-accountList").click()

    # Email gir
    email_field = driver.find_element(By.ID, "ap_email")
    email_field.send_keys(email)
    driver.find_element(By.ID, "continue").click()

    # Şifre gir
    password_field = driver.find_element(By.ID, "ap_password")
    password_field.send_keys(password)
    driver.find_element(By.ID, "signInSubmit").click()

    # Oturum açıldıktan sonra arama çubuğuna "samsung" yaz ve enter'a bas
    search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
    search_bar.send_keys("samsung")
    search_bar.send_keys(Keys.RETURN)

    # Bir süre bekle ve sonuçları kontrol et
    time.sleep(3)
    assert "samsung" in driver.title.lower(), "Arama sonuçları sayfası doğru yüklenmedi!"

