import pytest
import param
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    pytest.driver.implicitly_wait(10)
# Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.set_window_size(1080, 800)
    # pytest.driver.maximize_window()
    yield pytest.driver
    pytest.driver.quit()


def test_show_my_pets(testing):  # фикстуру добавляем в аргумент функции
    driver = testing  # транспортируем драйвер из фикстуры
# Вводим email
    driver.find_element(By.ID, 'email').send_keys(param.email)
# Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(param.password)
# Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
# Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
# Нажимаем на кнопку "Мои Питомцы"
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
# Проверяем, что мы оказались на странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h2').text == (param.username)


    driver.implicitly_wait(10)
    names = driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    driver.implicitly_wait(10)
    images = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets>table>tbody>tr>th>img')
    driver.implicitly_wait(10)
    types = driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[2]')
    driver.implicitly_wait(10)
    ages = driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[3]')

# тест1: Присутствуют все питомцы.

    user_stat_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html>body>div>div>div")))
    user_pets_count = int(user_stat_element.text.split("\n")[1].split(":")[1].strip())
    assert user_pets_count == len(names)


    pets_with_foto_count: int = 0
    pets_names = []
    pets_types = []
    pets_ages = []

    for i in range(len(names)):
        if images[i].get_attribute('src') != '':
            pets_with_foto_count += 1

# тест2: У всех питомцев есть имя, возраст и порода
        assert names[i].text != ''
        assert types[i].text != ''
        assert ages[i].text != ''

        if names[i].text != '':
            pets_names.append(names[i].text)

        if types[i].text != '':
            pets_types.append(types[i].text)

        if ages[i].text != '':
            pets_ages.append(ages[i].text)

# тест3: Хотя бы у половины питомцев есть фото.

    assert pets_with_foto_count >= user_pets_count / 2

# тест4: У всех питомцев разные имена.

    assert len(pets_names) == len(set(pets_names))

# тест5: В списке нет повторяющихся питомцев.

    assert len(set(pets_names)) == user_pets_count or len(set(pets_types)) == user_pets_count or len(
        set(pets_ages)) == user_pets_count
