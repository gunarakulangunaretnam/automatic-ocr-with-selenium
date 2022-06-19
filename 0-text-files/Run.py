import os 
import shutil
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


engine = pyttsx3.init()
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"  # female
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"  # male
engine.setProperty('voice', en_voice_id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)

def talk_function(audio):
	print("Computer: {}".format(audio))
	engine.say(audio)
	engine.runAndWait()

working_dir_path = os.path.dirname(os.path.realpath(__file__))
supported_extensions = ['.jpg','.jpeg','.png','.tiff','jfif','gif','.bmp']

default_download_directory = "{}\\Output_Data\\".format(working_dir_path)

options = webdriver.ChromeOptions()


prefs = {
"download.default_directory": default_download_directory,
"download.prompt_for_download": False,
"download.directory_upgrade": True
}

options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)
driver.get("https://www.onlineocr.net/")
driver.maximize_window()
driver.execute_script("window.scrollTo(0, 300)") 


input_dir = "{}\\Input_Data\\".format(working_dir_path)
output_dir = "{}\\Output_Data\\".format(working_dir_path)

for file in os.listdir(output_dir):
	os.remove(output_dir+file)

index = 1

for file in os.listdir(input_dir):
	extension = os.path.splitext(file)[1]
	
	if extension in supported_extensions:
		os.rename(os.path.join(input_dir, file), os.path.join(input_dir, ''.join(["Data_Sheet_{}".format(index), '.jpg'])))
		index = index + 1

	else:
		os.remove(input_dir+file)


path, dirs, files = next(os.walk(input_dir))
Total_Files = len(files)


talk_function("Hello, This is GR auto task assistant. The Process is starting.")

print("\n")


Report_No = 1

for file in os.listdir(input_dir):

	print("Processing... ({}/{})".format(Report_No,Total_Files))

	select = Select(driver.find_element_by_id('MainContent_comboOutput'))
	select.select_by_visible_text('Text Plain (txt)')	

	driver.find_element_by_id('fileupload').send_keys(input_dir+file)

	while True:
		span_element = driver.find_element_by_id("MainContent_lbProgressFile2")
		
		if(span_element.text.strip() == file):
			break
	
	driver.find_element_by_id('MainContent_btnOCRConvert').click()

	while True:
		try:
			convert_btn = driver.find_element_by_id('MainContent_btnOCRConvert')
			disabledVal = convert_btn.get_attribute("disabled")
			text_val = convert_btn.get_attribute('value')

			if text_val == "CONVERT" and disabledVal == "true":
				break
			
		except Exception as e:
			pass


	driver.find_element_by_id('MainContent_lnkBtnDownloadOutput').click()

	Report_No = Report_No + 1


talk_function("The process is completed.")
	









