#! python3
##

'''
README

First fill in the filepath to the chromedriver around line 122

You will start at the main menu:
Running2win Python Application

1. Quick Log   		<--- Enter 1 to log your workout info from this prompt.  All the info will be entered into r2w automatically (headless)
2. Log Workout 		<--- Enter 2 to manually log a workout.  The program will pull up a New Workout page
3. Open Homepage 	<--- Enter 3 to go to the homepage.  The program will just log you in

What would you like to do?:


Quick Log Notes:

Date - Enter through the date prompt to select the current day. Otherwise enter +/- the # of days (Ex. -6 would be six days ago)
AM Run - Default is PM run. Enter y or yes to log it as an AM run
Workout Type - Default is Normal Run.  Enter the corresponding number if you want to select a different one
Shoe Type - This really only works if you keep track of shoes.  It also stores the list on your computer using Shelve.  You can enter through and it will not log a shoe


'''


import sys
import shelve
import time
import os
import configparser
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import Select


#initial menu
def main_menu():
	print('Running2win Python Application\n')
	print('1. Quick Log\n2. Log Workout\n3. Open Homepage\n')
	while True:
		choice = input('What would you like to do?: ')
		if choice in ['q', 'quit']:			#option to exit.  good for if I accidentally choose to log another workout
				return('quit')
		try:
			if int(choice) in [1,2,3]:
				break
		except:
			pass
	return int(choice)

#pick which shoes
def shoe_picker():
	try:
		shelfFile = shelve.open('shoe_shelf')
		shoe_list = shelfFile['shoe_list']
		shelfFile.close()
	except:
		return	
	
	print('Shoe Selection:')
	for i in range(len(shoe_list)):
		print(str(i+1) + '. ' + shoe_list[i])	# plus 1 here for the list formatting
	try:	
		shoe_choice = int(input('\nwhich shoe?: '))-1 # minus 1 here to adjust for the +1 above  # null is entered, do not log a shoe.  return 0
	except ValueError:
		print('No shoe selected\n')
		return 0
	if shoe_choice == -1:
		print('most recent shoe selected\n')
		return 1
	else:
		print(shoe_list[shoe_choice] + ' selected\n')

		return shoe_list[shoe_choice].split('(')[0]			# return the name of the shoe up to the 1st parentheses


#this will create an INI config file that stores your logins if none could be found.  the user should only have to do this once
def create_config(reset = False):
	config = configparser.ConfigParser()
	if not reset:
		print('Welcome to the r2w python script. Please enter your login credentials below.')
	username = input('Username: ')
	password = input('Password: ')
	config['r2w'] = {'username' : username, 'pw' : password}
	with open('r2wconfig.ini', 'w') as configfile:
		config.write(configfile)
	print('\n\nVerifying Credentials...')
	driver = r2w_login(home = True, test = True)
	return




#fire up r2w and pull up workout entry page if home = False
def r2w_login(home = False, headless = True, test = False):		#headless controls whether or not we use phantomjs for quick log

	import configparser
	config = configparser.ConfigParser()
	config.read('r2wconfig.ini')
	# define constants.  I wouldve put this part in another function, but it's a lot of variable passing
	login_info = {}
	login_info['url'] = 'http://www.running2win.com/index.asp'
	login_info['username'] = config['r2w']['username']

	login_info['pw'] = config['r2w']['pw']

	username_element_name = "txtUsername"
	pw_element_name = "txtPassword"
	login_button_element_name = "btnLogin"
	login_info['login_button_text'] = "Log In"


	# open r2w and go through the login process
	if headless:
		driver = webdriver.PhantomJS() # or add to your PATH
		driver.set_window_size(1024, 768) # optional
	else:
		driver = webdriver.Chrome("") #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Insert the filepath
	driver.get(login_info['url'])

	driver.find_element_by_link_text(login_info['login_button_text']).click()
	time.sleep(1) # let the page load
	driver.find_element_by_name(username_element_name).send_keys(login_info['username'])
	driver.find_element_by_name(pw_element_name).send_keys(login_info['pw'])
	driver.find_element_by_name(login_button_element_name).click()	
	if test:
		try:
			time.sleep(1)	#remove
			_ = driver.find_element_by_link_text(login_info['username'])
			cls()
			print('Username/Password Accepted')
			time.sleep(2)
			return
		except:
			cls()
			print('Your logins may be incorrect.  Please re-enter them.')
			create_config(reset = True)
			print('\nRestarting Program...')
				

	if not home:
		open_wo(driver)
		return driver
	else:
		while True:
			_ = input('\n\nq to close: ')
			if _ == 'q':
				sys.exit()


def open_wo(driver):
	time.sleep(1)
	driver.find_element_by_link_text("MENU").click()
	time.sleep(1)
	driver.find_element_by_link_text("Log a Workout").click()
	
def am_run_prompt():
	if input('AM run? (y/n):') == 'y':
		print('AM run\n')
		return True
	else:
		print('PM run\n')
		return False


#get current date
# enter 1 or -2 
def date_prompt(n = ''):
	i = datetime.now()
	run_date = "{}/{}/{}".format(i.month, i.day, i.year)
	date_input = input('Today? ({}): '.format(run_date))  
	try:
		n = int(date_input)
		i = datetime.now() + timedelta(days=n)
	except:
		pass

	run_date = "{}/{}/{}".format(i.month, i.day, i.year)
	print('{} selected\n'.format(run_date))

	return run_date

def run_type_prompt():
	workout_types = ['', 'Normal Run', 'Long Run', 'Hill Training', 'Tempo', 'Speed Training', 'Fartlek', 'Interval Workout']
	print('Workout Types:')
	for workout in workout_types[1:]:
		print('{}. {}'.format(workout_types.index(workout), workout))
	while True:
		workout_choice = input('\nWhich kind of workout? ')
		if workout_choice == '':
			print('Normal Run selected\n')
			return
		try:
			workout_choice = workout_types[int(workout_choice)]
			print('{} selected\n'.format(workout_choice))
			return workout_choice
		except:
			pass

def cls(): 			
	#something I found that clears the screen    
	os.system("cls")


def distance_prompt():
	while True:
		try:
			run_distance = str(float(input('How Far?: ')))
			print('{} miles\n'.format(run_distance))
			return run_distance
		except:
			pass


def log_wo(driver, wo_info):	
	#find fields and create objects for them
	
	date_field = driver.find_element_by_name('txtWODate')
	comments_field = driver.find_element_by_name('txtComments')
	distance_field = driver.find_element_by_name('txtDistance')
	tod_list = Select(driver.find_element_by_id('lstTimeOfDay'))
	run_type_list = Select(driver.find_element_by_id('lstRunTypes'))
	shoes = Select(driver.find_element_by_id('lstShoes'))
	print('Entering Workout Data...')

	#enter date
	date_field.clear()
	date_field.send_keys(wo_info['run_date'])

	#set time of day
	if wo_info['am_run_yn']:	#select AM run if True 
		tod_list.select_by_value('1')

	#enter distance
	distance_field.clear()
	distance_field.send_keys(wo_info['run_distance'])

	#enter run type
	if wo_info['run_type']:
		run_type_list.select_by_visible_text(wo_info['run_type'])


	#enter comments
	comments_field.send_keys(wo_info['comments'])

	#select shoes
	shelfFile = shelve.open('shoe_shelf')

	if wo_info['shoe_choice']:
		shoe_list = [o.text for o in shoes.options]
		shelfFile['shoe_list'] = shoe_list[1:5]
		if wo_info['shoe_choice'] == 1:
			shoes.select_by_value(1)
		else:
			for shoe in shoe_list:
				if wo_info['shoe_choice'] in shoe:			
					shoes.select_by_visible_text(shoe)
	shelfFile.close()
	
	save_button = driver.find_element_by_name('btnSave')
	save_button.click()
	
	print('Workout Saved...')

	return
	

def quick_log_prompt():
	cls()  		#clear the screen so I can look at a clean 'Quick Log' prompt
	wo_info = {}	#create dictionary to hold wo info
	print('----- Running2Win Quick Log -----\n')
	wo_info['run_date'] = date_prompt()
	wo_info['am_run_yn'] = am_run_prompt()
	wo_info['run_distance'] = distance_prompt()
	wo_info['run_type'] = run_type_prompt()
	wo_info['shoe_choice'] = shoe_picker()
	wo_info['comments'] = input('Comments: ')

	return wo_info




def main():

	if not os.path.isfile('r2wconfig.ini'):
		create_config()


	#main prompt
	while True:
		cls()
		choice = main_menu()

		if choice == 1: # quick log

			wo_info = quick_log_prompt()   #go into quick log where I can enter the info from cmd prompt
			#stored all the wo info into a dictionary now i can pass that into the log workout function
			driver = r2w_login() #log into r2w and pull up workout page
			log_wo(driver, wo_info)
			if input("log something else? (y/n): ").lower() in ['n', 'no', '', 'quit', 'q']:
				break

		elif choice == 2: # log workout in detail.  this will pull up a log workout page for me to enter the data
			driver = r2w_login(headless = False)
			_ = input('press any key to exit...')
			break

		elif choice == 3: # open homepage and stop there
			driver = r2w_login(home = True, headless = False)
			_ = input('press any key to exit...') 
			break

		elif choice == 'quit':
			break

	try:
		if driver:
			print('quitting driver')
			driver.quit()
	except:
		pass
	print('\nExiting r2w application...\n')





main()

	

