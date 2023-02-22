from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import random as rn


username = "kunasyl"
password = "Kunasyl123."

def get_driver():
    browser = Chrome("E:/Master's degree/Software testing/6/chromedriver_win32/chromedriver.exe")
    return browser


driver = get_driver()

url = "https://st-online-store.herokuapp.com/admin"
card = "https://st-online-store.herokuapp.com/card"
home_page_url = "https://st-online-store.herokuapp.com/products"
register_url = "https://st-online-store.herokuapp.com/users/new"
login_url = "https://st-online-store.herokuapp.com/login"
logout_url = "https://st-online-store.herokuapp.com/logout"
home_admin_page = "https://st-online-store.herokuapp.com/admin"
new_product_url = "https://st-online-store.herokuapp.com/products/new"
edit_products_url = "https://st-online-store.herokuapp.com/products/edit"


product_id = f'test  {rn.randint(1, 10)}'



''' 1. Register an account '''

def test_user_register():
    driver.get(register_url)
    driver.find_element(By.ID, 'user_name').send_keys(username)
    driver.find_element(By.ID, 'user_password').send_keys(password)
    driver.find_element(By.ID, 'user_password_confirmation').send_keys(password)
    driver.find_element(By.NAME, 'commit').click()
    time.sleep(3)

    assert driver.current_url == home_page_url, "User registration successed"



''' 2. Login to the system '''

def test_login():
    driver.get(login_url)
    driver.find_element(By.ID, 'name').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.NAME, 'commit').click()
    time.sleep(3)

    assert driver.current_url == home_page_url, "User logged in"


def login():
    driver.get(login_url)
    driver.find_element(By.ID, 'name').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.NAME, 'commit').click()



''' 3. Logout from the system '''

@login
def test_logout():
    driver.get(logout_url)
    time.sleep(3)

    assert driver.current_url == home_admin_page, "User logged out"



''' 4. Delete an account '''

@login
def test_delete_acc():
    driver.get(url)
    driver.find_element(By.XPATH, "delete").click()

    assert driver.current_url == login_url, "Account was successfully deleted"



''' 5. Add products '''

@login
def test_add_product():
    driver.get(new_product_url)
    driver.find_element(By.ID, "product_title").send_keys(product_id)
    driver.find_element(By.ID, "product_description").send_keys('test')
    driver.find_element(By.ID, "product_price").send_keys(100)
    driver.find_element(By.NAME, 'commit').click()
    time.sleep(3)

    assert driver.current_url == home_page_url, "User successfully added product"



''' 6. Edit products '''

@login
def test_edit_product():
    driver.get(edit_products_url)
    new_product_title = f"test"
    driver.find_element(By.XPATH, new_product_title).send_keys("test edited ")
    time.sleep(3)
    notif = driver.find_element(By.XPATH, "//*[@id=\"notice\"]").text
    
    assert notif == "Product was successfully edited.", "Notification"



''' 7. Delete products '''

@login
def test_delete_product():
    driver.get(home_page_url)
    product_title = f"//*[@id=\"{product_id}\"]/td[4]/a"
    driver.find_element(By.XPATH, product_title).click()
    time.sleep(3)
    notif = driver.find_element(By.XPATH, "//*[@id=\"notice\"]").text
    assert notif == "User deleted the product", "Notification"



''' Add products to the cart '''

@login
def test_add_product():
    driver.get(home_page_url + "product/test")
    driver.find_element(By.CLASS_NAME, "add-to-card").click()
    assert driver.current_url == login_url, "User successfully added the product"



''' Increase/decrease the quantity of products in the cart '''

@login
def test_increase_quantity():
    driver.get(home_page_url + "card")
    new_product_title = f"quantity"
    driver.find_element(By.XPATH, new_product_title).send_keys("8")
    time.sleep(3)
    notif = driver.find_element(By.XPATH, "//*[@id=\"notice\"]").text
    assert notif == "Product was successfully edited.", "Notification"



driver.close()
driver.quit()
