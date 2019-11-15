from selenium import webdriver
import pandas as pd
import selenium.webdriver.support.ui as ui
import time
import csv
driver = webdriver.Chrome()
driver.get("http://psd.bits-pilani.ac.in/Student/ViewActiveStationProblemBankData.aspx")
username = input("Enter the username here:\n")
passwrd = input("enter the password:\n")
driver.find_element_by_id("TxtEmail").send_keys(username)
driver.find_element_by_id ("txtPass").send_keys(passwrd)
driver.find_element_by_id("Button1").click()
#go to the PS Page
driver.get("http://psd.bits-pilani.ac.in/Student/ViewActiveStationProblemBankData.aspx")

wait = ui.WebDriverWait(driver,10)

wait.until(lambda driver: driver.find_element_by_id('prohid'))


stationId_element = driver.find_elements_by_id("PBData")
numberofstations = int(input("Enter the current number of Stations\n"))
locations = []
print("Enter the Station Location Preferred(Enter line by line and type 'done' without quotes when you are done):\n")

while 1:
    station = input()
    if station.lower()=='done':
        break
    locations.append(station.lower())

#testing
print(locations)

stationInfo = []
totalInfo = []
stationInfo.append('Station Name')
stationInfo.append('Location')
stationInfo.append('Stipend')
stationInfo.append('Disciplines allowed')
totalInfo.append(stationInfo)
stationInfo = []
# for x in [1,2,3,4]:

for x in range(1,numberofstations+1,1):
    #xpath for the location of ps
    loc = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[2]/div/table/tbody/tr["+str(x)+"]/td[2]")

    #see if it is in the list of locations
    if loc.text.lower() not in locations:
        continue

    #get the name of the station
    name = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[2]/div/table/tbody/tr["+str(x)+"]/td[3]")

    #To get the stipend clicking the view button
    driver.find_element_by_xpath("/html/body/form/div[4]/div/div[2]/div/table/tbody/tr["+str(x)+"]/td[6]/a").click()
    #wait till the stipend field is not empty
    wait.until(lambda driver: len(driver.find_element_by_xpath('/html/body/form/div[5]/div[1]/div/div[2]/div/table/tbody/tr[1]/td[3]').text)!=0)

    #get the stipend
    stipend = driver.find_element_by_id("Stipend")

    discipline = driver.find_element_by_xpath('/html/body/form/div[5]/div[1]/div/div[2]/div/table/tbody/tr/td[7]')

    #create the row that will be dumped in the csv
    stationInfo.append(name.text)
    stationInfo.append(loc.text)
    stationInfo.append(stipend.text)
    stationInfo.append(discipline.text)
    #Testing purpose
    print(stationInfo)
    totalInfo.append(stationInfo)
    stationInfo = []

    #click the cross button on the view page
    element = driver.find_element_by_xpath('/html/body/form/div[5]/div[1]/div/div[1]/button/i')
    driver.execute_script("arguments[0].click();", element)
    #wait for it to fade (this could be optimized)
    time.sleep(1)

#dump the list into the csv
with open("preference.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(totalInfo)
