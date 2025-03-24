from flask import render_template, request, redirect,jsonify, make_response,Response,json
#from app import app
from datetime import datetime
import time
import os
from werkzeug.utils import secure_filename
import pymongo
from bson.objectid import ObjectId
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime 
import pandas as pd

import pprint
from selenium.common.exceptions import NoSuchElementException
from my_functions import find_stat,find_team_stat
from links import links_23_season,links23_male_post
client=pymongo.MongoClient()
mydb = client["DeedLeague"] 
mycol=mydb['current_game']

#PATH="C:\Program Files\chromedriver.exe"
driver=webdriver.Chrome()
driver.maximize_window()
link_game="https://fibalivestats.dcd.shared.geniussports.com/u/MNBA/2376927/" #"https://fibalivestats.dcd.shared.geniussports.com/u/MNBA/2591969/"


driver.get(link_game)
#print(links23_male_post[gms]) #debug
# wait 3 seconds
time.sleep(2)
driver.find_element(By.XPATH,"//a[contains(@href,'bs.html')]").click()
time.sleep(2)
#collecting entire game stats

#scores by quarter
team1_first_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_p1_score']").text
team1_second_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_p2_score']").text
team1_third_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_p3_score']").text
team1_fourth_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_p4_score']").text
team1_ot_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_ot_score']").text
t1_ot=team1_ot_qtr if(team1_ot_qtr!="") else 0
t1_qtr={
    "first":int(team1_first_qtr),
    "second":int(team1_second_qtr),
    "third":int(team1_third_qtr),
    "fourth":int(team1_fourth_qtr), 
    "ot":int(t1_ot) 
}

team2_first_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_p1_score']").text
team2_second_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_p2_score']").text
team2_third_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_p3_score']").text
team2_fourth_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_p4_score']").text
team2_ot_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_ot_score']").text
t2_ot=team2_ot_qtr if(team2_ot_qtr!="") else 0
t2_qtr={
    "first":int(team2_first_qtr),
    "second":int(team2_second_qtr),
    "third":int(team2_third_qtr),
    "fourth":int(team2_fourth_qtr), 
    "ot":int(t2_ot) 
}   


team1_name=driver.find_element(By.XPATH,"//div[contains(@class,'team-0-bs')]/div[2]/span").text
team1_score=int(driver.find_element(By.XPATH,"//div[contains(@class,'team team-0')]/div[5]/span").text)
team2_name=driver.find_element(By.XPATH,"//div[contains(@class,'team-1-bs')]/div[2]/span").text
team2_score=int(driver.find_element(By.XPATH,"//div[contains(@class,'team team-1')]/div[5]/span").text)
match_type=driver.find_element(By.XPATH,"//div[contains(@class,'matchDetails col col-12 align-center')]/div/p").text

game_details=date_str=driver.find_element(By.XPATH,"//div[contains(@class,'matchDetails col col-12 align-center')]/div[2]/h6").text
if(game_details=="GAME DETAILS"):
    date_str=driver.find_element(By.XPATH,"//div[contains(@class,'matchDetails col col-12 align-center')]/div[2]/p").text
else:
    date_str=driver.find_element(By.XPATH,"//div[contains(@class,'matchDetails col col-12 align-center')]/div[3]/p").text
dates=date_str.split()[-1]
date=dates.split("/")
date_string="20"+date[2]+"/"+date[1]+"/"+date[0]
format_string="%Y/%m/%d"
date_obj=datetime.strptime(date_string,format_string)

    
#----------> collecting each player stat
rows1=driver.find_elements(By.XPATH,"//tbody[contains(@class,'on-court team-0-person-container')]/tr")
## Эзэн багийн гарааны таван тоглогчийн статистик
num_of_rows=len(rows1)
t1_players=[]
t1_bench=[]
team1=[]
for kk in range(1,num_of_rows+1):
    try:
        xpath="//tbody[contains(@class,'on-court team-0-person-container')]/tr["+str(kk)+"]"
        #xpath="//tbody[contains(@class,'on-court team-0-person-container')]/tr[2]"
        sel_row=driver.find_element(By.XPATH,"//tbody[contains(@class,'on-court team-0-person-container')]/tr["+str(kk)+"]")
        
        if(sel_row.get_attribute("class"))!="player-row row-not-used":
            player=find_stat(driver,xpath,team1_name,1)
            t1_players.append(player)
            #print(player)
            #mycol.insert_one(player)
    except NoSuchElementException:
        break  
rows2=driver.find_elements(By.XPATH,"//div[contains(@class,'boxscorewrap team-0-bs')]/table/tbody[2]/tr") 
num_of_rows2=len(rows2) 
for jj in range(1,num_of_rows2+1):  
    try:
        xpath1="//div[contains(@class,'boxscorewrap team-0-bs')]/table/tbody[2]/tr["+str(jj)+"]"
        #xpath="//tbody[contains(@class,'on-court team-0-person-container')]/tr[2]"
        sel_row1=driver.find_element(By.XPATH,"//div[contains(@class,'boxscorewrap team-0-bs')]/table/tbody[2]/tr["+str(jj)+"]")
        
        if(sel_row1.get_attribute("class"))!="player-row row-not-used":
            player1=find_stat(driver,xpath1,team1_name,0)
            #print(player1)
            t1_players.append(player1)
            #mycol.insert_one(player1)
    except NoSuchElementException:
        break  
df=pd.DataFrame(t1_players)  
print(df)  
rows3=driver.find_element(By.XPATH,"//div[contains(@class,'boxscorewrap team-0-bs')]/table/tbody[3]/tr[2]")  
try:
    xpath2="//div[contains(@class,'boxscorewrap team-0-bs')]/table/tbody[3]/tr[2]"
    #xpath="//tbody[contains(@class,'on-court team-0-person-container')]/tr[2]"
    sel_row2=driver.find_element(By.XPATH,"//div[contains(@class,'boxscorewrap team-0-bs')]/table/tbody[3]/tr[2]")
    stat_path1="//div[contains(@class,'team-stats team-0-ts')]"
    team1_data=find_team_stat(driver,xpath2,stat_path1)
    team1.append(team1_data)
    #print(team1)

except NoSuchElementException:
    pass    


######----------------------------------TEAM2------DETAIL--------------------------
rows_t2_1=driver.find_elements(By.XPATH,"//tbody[contains(@class,'on-court team-1-person-container')]/tr")
num_of_rows=len(rows_t2_1)
t2_players=[]
t2_bench=[]
team2=[]
for kk in range(1,100):
    try:
        xpath_t2="//tbody[contains(@class,'on-court team-1-person-container')]/tr["+str(kk)+"]"
        sel_row_t2=driver.find_element(By.XPATH,"//tbody[contains(@class,'on-court team-0-person-container')]/tr["+str(kk)+"]")
        
        if(sel_row_t2.get_attribute("class"))!="player-row row-not-used":
            player_t2=find_stat(driver,xpath_t2,team2_name,1)
            t1_players.append(player_t2)
        
    except NoSuchElementException:
        break 
rows2_t2=driver.find_elements(By.XPATH,"//div[contains(@class,'boxscorewrap team-1-bs')]/table/tbody[2]/tr") 
num_of_rows2=len(rows2_t2) 
for jj in range(1,num_of_rows2+1):  
    try:
        xpath1_t2="//div[contains(@class,'boxscorewrap team-1-bs')]/table/tbody[2]/tr["+str(jj)+"]"
        #xpath="//tbody[contains(@class,'on-court team-0-person-container')]/tr[2]"
        sel_row1_t2=driver.find_element(By.XPATH,"//div[contains(@class,'boxscorewrap team-1-bs')]/table/tbody[2]/tr["+str(jj)+"]")
        
        if(sel_row1_t2.get_attribute("class"))!="player-row row-not-used":
            player1_t2=find_stat(driver,xpath1_t2,team2_name,0)
            #print(player1)
            t1_players.append(player1_t2)
            #mycol.insert_one(player1)
    except NoSuchElementException:
        break  
rows3_t2=driver.find_element(By.XPATH,"//div[contains(@class,'boxscorewrap team-1-bs')]/table/tbody[3]/tr[2]")  
try:
    xpath2_t2="//div[contains(@class,'boxscorewrap team-1-bs')]/table/tbody[3]/tr[2]"
    #xpath="//tbody[contains(@class,'on-court team-0-person-container')]/tr[2]"
    sel_row2=driver.find_element(By.XPATH,"//div[contains(@class,'boxscorewrap team-0-bs')]/table/tbody[3]/tr[2]")
    stat_path2="//div[contains(@class,'team-stats team-1-ts')]"
    team2_data=find_team_stat(driver,xpath2_t2,stat_path2)
    team2.append(team2_data)
    #print(team2)

except NoSuchElementException:
    pass       


######----------------------------------add-to- dictionary----------------------------------------    
game={
        "_id":"ongoing",
        "t1_name"    : team1_name,
        "t1_score"   : team1_score,
        "t2_name"    : team2_name,
        "t2_score"   : team2_score,
        "season"     : "2025",
        "male"       : 1, 
        "date"       : date_obj,    
        "t1_players" : t1_players,
        "team1_stat" : team1_data,
        "team2_stat" : team2_data,
        "t1_qtr"     : t1_qtr,
        "t2_qtr"     : t2_qtr 
        } 
#game_rec=mycol.find_one({},{_id:1})
print(game)
update_query={'_id':"ongoing"}
update_operation={'$set':game}
mycol.update_one(update_query,update_operation)    
#mycol.insert_one(game)
driver.quit()