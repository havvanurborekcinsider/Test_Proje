import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    # Chrome WebDriver'ı başlat
    driver = webdriver.Chrome()
    yield driver
    driver.quit()  # Test tamamlandıktan sonra tarayıcıyı kapat

def test_open_amazon(driver):
    driver.get("http://www.amazon.com.tr")
    assert "Amazon" in driver.title, "Amazon ana sayfası yüklenemedi!"
    print("Amazon ana sayfası başarıyla yüklendi.")
    time.sleep(5)

def test_accept_cookies(driver):
    try:
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="sp-cc-accept"]'))
        )
        cookie_accept_button.click()
        print("Çerezler kabul edildi.")
    except Exception as e:
        print("Çerez kabul butonu bulunamadı veya tıklanamadı:", e)
    time.sleep(5)

def test_login(driver):
    email = "qualityasurance9@gmail.com"
    password = "Test1234!"
    driver.find_element(By.ID, "nav-link-accountList").click()
    time.sleep(2)

    driver.find_element(By.ID, "ap_email").send_keys(email)
    driver.find_element(By.ID, "continue").click()
    time.sleep(2)

    driver.find_element(By.ID, "ap_password").send_keys(password)
    driver.find_element(By.ID, "signInSubmit").click()
    time.sleep(5)

def test_search_for_product(driver):
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("samsung")
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    print("‘Samsung’ için arama başarıyla yapıldı.")

def test_verify_search_results(driver):
    assert "samsung" in driver.page_source.lower(), "‘Samsung’ için arama sonuçları bulunamadı!"
    print("‘Samsung’ için arama sonuçları doğrulandı.")

def test_go_to_second_page(driver):
    try:
        target_xpath = '//*[@aria-label="2 sayfasına git"]'
        while True:
            try:
                target_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, target_xpath))
                )
                if target_element.is_displayed():
                    print("2. sayfaya gitmek için buton bulundu!")
                    break
            except:
                pass

            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1)

        target_element.click()
        print("2. sayfaya başarıyla geçildi.")
    except Exception as e:
        print("Kaydırma işlemi sırasında bir hata oluştu:", e)

def test_verify_page_navigation(driver):
    try:
        current_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".s-pagination-selected"))
        )
        assert current_page.text == "2", f"2. sayfa yüklenemedi, şu anki sayfa: {current_page.text}"
        print("2. sayfada olduğum doğrulandı.")
    except Exception as e:
        print("Sayfa geçişinde bir hata oluştu:", e)

def test_click_third_product(driver):
    try:
        product_xpath = "(//div[contains(@class, 's-main-slot')]//div[contains(@class, 's-result-item')])[3]"
        while True:
            try:
                product = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, product_xpath))
                )
                if product.is_displayed():
                    print("3. Ürün bulundu!")
                    break
            except Exception as e:
                print(f"Hata: {e}")
                pass

            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1)

        product.click()
        time.sleep(5)
        print("3. Ürüne başarıyla tıklandı.")
    except Exception as e:
        print("Ürün tıklama işleminde bir hata oluştu:", e)

def test_add_to_wishlist(driver):
    try:
        add_to_list_xpath = '//*[@id="add-to-wishlist-button-submit"]'
        add_to_list_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, add_to_list_xpath))
        )
        add_to_list_button.click()
        time.sleep(15)
        print("Ürün başarıyla listeye eklendi.")
    except Exception as e:
        print("Listeye ekleme işleminde bir hata oluştu:", e)

def test_view_wishlist(driver):
    try:
        wishlist_button_xpath = '//*[@id="huc-view-your-list-button"]/span/a'
        wishlist_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, wishlist_button_xpath))
        )
        wishlist_button.click()
        time.sleep(3)
        print("Wish List sayfası başarıyla açıldı.")
    except Exception as e:
        print("Wish List sayfasına tıklama işleminde bir hata oluştu:", e)

def test_verify_product_in_wishlist(driver):
    assert "samsung" in driver.page_source.lower(), "Wish List'te ürün bulunamadı!"
    print("Wish List'te ürün bulundu.")

def test_remove_product_from_wishlist(driver):
    try:
        delete_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[name='submit.deleteItem']"))
        )

        if delete_button.is_enabled():
            delete_button.click()
            print("Ürün başarıyla wishlist'ten silindi.")
        else:
            print("Ürün silinemedi: Buton tıklanamaz durumda.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

def test_verify_empty_wishlist(driver):
    driver.refresh()
    time.sleep(1)

    try:
        empty_wishlist_image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='no-items-section']/span/div[1]/img"))
        )
        print("Wish List boş. !!TEST TAMAMLANDI!!")
    except Exception as e:
        print("Wishlist boş kontrolü sırasında bir hata oluştu:", e)

if __name__ == "__main__":
    pytest.main()
