#! python3

#you need to run this before you use the r2w Quick Log option.  It finds your shoe list on r2w and stores it on your machine
#you can also run this to update the shoe list if you've been manually logging

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import shelve
import time


login_info = {}
login_info['url'] = 'http://www.running2win.com/index.asp'

login_info['username'] = #ENTER USERNAME <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
login_info['fullp'] = #ENTER PASSWORD <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

username_element_name = "txtUsername"
pw_element_name = "txtPassword"
login_button_element_name = "btnLogin"
login_info['login_button_text'] = "Log In"

driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(1024, 768) # optional

driver.get(login_info['url'])
driver.find_element_by_link_text(login_info['login_button_text']).click()
time.sleep(1) # let the page load
driver.find_element_by_name(username_element_name).send_keys(login_info['username'])
driver.find_element_by_name(pw_element_name).send_keys(login_info['fullp'])
driver.find_element_by_name(login_button_element_name).click()

#time.sleep(1)
driver.find_element_by_link_text("MENU").click()
#time.sleep(1)
driver.find_element_by_link_text("Log a Workout").click()

shoes = Select(driver.find_element_by_id('lstShoes'))

shelfFile = shelve.open('shoe_shelf')
shoe_list = [o.text for o in shoes.options]
shelfFile['shoe_list'] = shoe_list[1:5]

shelfFile.close()
for shoe in shoe_list[1:5]:
	print(shoe)

driver.quit()