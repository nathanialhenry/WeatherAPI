from selenium import webdriver
import os, json, requests

# Uses local chromedriver for web scrape
currentdirectory = os.getcwd()
chromepath = currentdirectory + r"\chromedriver.exe"
# Gets the weather.com webpage using chromedriver
driver = webdriver.Chrome(chromepath)
driver.get("https://weather.com/weather/tenday/l/Vancouver+British+Columbia+Canada?canonicalCityId=3c9f9c7dd098e7719388ee7fc44e3d1de1aeee14a428910d45efe3bd73a31c0d")
# Pulls required information for weather rows and the list of days
weather_table = driver.find_elements_by_class_name('_-_-components-src-atom-Disclosure-Disclosure--themeList--1Dz21')
day_list = driver.find_elements_by_class_name('_-_-components-src-molecule-DaypartDetails-DetailsSummary-DetailsSummary--daypartName--kbngc')
# Creates list objects for later json creation
hightemp_list = []
lowtemp_list = []
status_list = []
percipitation_list = []
# Iterates over the rows in weather table to pull highs,lows, and percipitation from webpage (status is broken atm)
# Uses a Try/Catch just in case there is missing data in any of the rows
for row in weather_table:
    try:
        hightemp_elem = row.find_element_by_class_name('_-_-components-src-molecule-DaypartDetails-DetailsSummary-DetailsSummary--highTempValue--3PjlX')
        hightemp_list.append(hightemp_elem)
        lowtemp_elem = row.find_element_by_class_name('_-_-components-src-molecule-DaypartDetails-DetailsSummary-DetailsSummary--lowTempValue--2tesQ')
        lowtemp_list.append(lowtemp_elem)
        percipitation_elem = row.find_elements_by_xpath('//span [@data-testid="PercentageValue"]')
        percipitation_list.append(percipitation_elem) 
        # status_elem = row.find_element_by_xpath('//span [@class="_-_-components-src-molecule-DaypartDetails-DetailsSummary-DetailsSummary--extendedData--307Ax"]')
        # status_list.append(status_elem)
    except:
        continue
# Delete these indexes from percipitation list as they pull incorrect information
del percipitation_elem [1]
del percipitation_elem [1]
# Create new percipitation list of only tabled information (lots of null value in previous list)
ref_percipitation_list = []
for i in percipitation_elem:
    if i.text != '':
        ref_percipitation_list.append(i.text)
# Creates dictionary object for information
vancouverweather = {}
vancouverweather['weatherdata'] = []
# Iterates over number of rows, adding weather information per day/row
for row in range(15):
    day = day_list[row]
    hightemp = hightemp_list[row]
    temphightemp = hightemp.text
    refachightemp = temphightemp[0:2]
    lowtemp = lowtemp_list[row]
    templowtemp = lowtemp.text
    refaclowtemp = templowtemp[0:2]
    status = "NA"
    percipitation = ref_percipitation_list[row]
    vancouverweather['{0}'.format(day.text)] = ({
        'hightemp':'{0}'.format(refachightemp),
        'lowtemp': '{0}'.format(refaclowtemp),
        'status' : '{0}'.format(status),
        'percipitation' : '{0}'.format(percipitation)
    })
# Sends json data to flask API, where it is saved into a file on server
# try:
#     sendpost = requests.post('http://127.0.0.1:5000/weather/post', json = vancouverweather)
#     print("Data Updated")
# except Exception as e:
#     print("An Exception has occurred: {0}".format(e))
try:
    sendpost = requests.post('http://weatherapi.eba-yymnwemy.us-west-2.elasticbeanstalk.com/post', json = vancouverweather)
    print("Data Updated")
except Exception as e:
    print("An Exception has occurred: {0}".format(e))
driver.quit()