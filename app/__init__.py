from flask import Flask
from flask import render_template, request, redirect,jsonify, make_response,Response,json
from datetime import datetime
import time
import os
import sys
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
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .my_functions import find_stat,find_team_stat ,find_brief,common_name,title_name
from .aggregate import avg_plr_stat,last_games

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

client=pymongo.MongoClient()
mydb = client["DeedLeague"] 
current_game=mydb['current_game']
mystat=mydb['full_stat']
link_archive=mydb['Links']
roster=mydb['roster2025']

app=Flask(__name__)
"""if app.config["ENV"]=="production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"]=="testing": 
    app.config.from_object("config.TestingConfig")
else:   
    app.config.from_object("config.DevelopmentConfig") """
##from app import current_game_stat
@app.route("/")
def index():
    print(app.config["DEBUG"])  
    return render_template('public/main.html')


@app.route('/returnjson', methods = ['GET']) 
def ReturnJSON(): 
    if(request.method == 'GET'): 
        data = { 
            "LeageName":"",
            "Logo":"System.Drawing.Bitmap",
            "Level":4,"HomeTeam":{"Id":1,"TeamName":"HOME","logourl":"/teamlogo/hometeam.png","ShortName":"СЭЛ",
                                  "TeamLogo":"System.Drawing.Bitmap","Score":27,"Fouls":1,"TimeOut":2,"Possession":0,"players":[{"id":0,"Lastname":"PLAYERNAME","Firstname":"BILGUUN","PlayerNumber":"12","image":"System.Drawing.Bitmap","Score":36,"Fouls":0,"Active":True,"StatisticBoardView":True},
                                  {"id":1,"Lastname":"PLAYERNAME","Firstname":"Enhbaatar","PlayerNumber":"11","image":"System.Drawing.Bitmap","Score":10,"Fouls":0,"Active":True,"StatisticBoardView":True},
                                  {"id":2,"Lastname":"PLAYERNAME","Firstname":"SANCHIR","PlayerNumber":"10","image":"System.Drawing.Bitmap","Score":40,"Fouls":0,"Active":True,"StatisticBoardView":True},
                                  {"id":3,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"3","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":True,"StatisticBoardView":True},
                                  {"id":4,"Lastname":"PLAYERNAME","Firstname":"Zorigoo","PlayerNumber":"4","image":"System.Drawing.Bitmap","Score":7,"Fouls":0,"Active":True,"StatisticBoardView":True},
                                  {"id":5,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"5","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                  {"id":6,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"6","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                  {"id":7,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"7","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                  {"id":8,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"8","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                  {"id":9,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"9","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                  {"id":10,"Lastname":"PLAYERNAME","Firstname":"Tului","PlayerNumber":"10","image":"System.Drawing.Bitmap","Score":26,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                  {"id":11,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"11","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                  {"id":12,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"12","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":False}]},
            "GuestTeam":{"Id":1,"TeamName":"AWAY","logourl":"/teamlogo/awayteam.png","ShortName":"РВТ","TeamLogo":"System.Drawing.Bitmap","Score":33
                ,"Fouls":3,"Possession":0,"TimeOut":2,"players":[{"id":0,"Lastname":"PLAYERNAME","Firstname":"olzii-orshih","PlayerNumber":"0","image":"System.Drawing.Bitmap","Score":26,"Fouls":0,"Active":1,"StatisticBoardView":True},
                                {"id":1,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"1","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":True,"StatisticBoardView":True},
                                {"id":2,"Lastname":"PLAYERNAME","Firstname":"Jargalmaa","PlayerNumber":"2","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":True,"StatisticBoardView":True},
                                {"id":3,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"3","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":True,"StatisticBoardView":True},
                                {"id":4,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"4","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":True,"StatisticBoardView":True},
                                {"id":5,"Lastname":"PLAYERNAME","Firstname":"Francesco","PlayerNumber":"5","image":"System.Drawing.Bitmap","Score":23,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                {"id":6,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"6","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                {"id":7,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"7","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                {"id":8,"Lastname":"PLAYERNAME","Firstname":"Trons","PlayerNumber":"99","image":"System.Drawing.Bitmap","Score":43,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                {"id":9,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"9","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                {"id":10,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"10","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                {"id":11,"Lastname":"PLAYERNAME","Firstname":"PLAYERNAME","PlayerNumber":"11","image":"System.Drawing.Bitmap","Score":0,"Fouls":0,"Active":False,"StatisticBoardView":True},
                                {"id":12,"Lastname":"PLAYERNAME","Firstname":"tran tran","PlayerNumber":"22","image":"System.Drawing.Bitmap","Score":13,"Fouls":0,"Active":False,"StatisticBoardView":False}]},
            "SessionTime":"02:54.4","AttackTime":15
        } 
  
        return jsonify(data) 


def add_current(link_game): 
      
        #PATH="C:\Program Files\chromedriver.exe"
       
        driver=webdriver.Chrome()
        driver.maximize_window()


        #link_game="https://fibalivestats.dcd.shared.geniussports.com/u/MNBA/2591969/"

       
        driver.get(link_game)
        #print(links23_male_post[gms]) #debug
        # wait 3 seconds
        time.sleep(1)
        driver.find_element(By.XPATH,"//a[contains(@href,'bs.html')]").click()
        time.sleep(1)
        #collecting entire game stats

        #scores by quarter
        """team1_first_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_p1_score']").text 
        team1_first_qtr=team1_first_qtr if(team1_first_qtr!="&nbsp") else 0
        team1_second_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_p2_score']").text
        team1_second_qtr=team1_second_qtr if(team1_second_qtr!="&nbsp") else 0
        team1_third_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_p3_score']").text
        team1_third_qtr=team1_third_qtr if(team1_third_qtr!="&nbsp") else 0
        team1_fourth_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_p4_score']").text
        team1_fourth_qtr=team1_fourth_qtr if(team1_fourth_qtr!="&nbsp") else 0
        team1_ot_qtr=driver.find_element(By.XPATH,"//span[@id='aj_1_ot_score']").text
        t1_ot=team1_ot_qtr if(team1_ot_qtr!="&nbsp") else 0
        t1_qtr={
            "first":int(team1_first_qtr),
            "second":int(team1_second_qtr),
            "third":int(team1_third_qtr),
            "fourth":int(team1_fourth_qtr), 
            "ot":int(t1_ot) 
        }

        team2_first_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_p1_score']").text
        team2_first_qtr=team2_first_qtr if(team2_first_qtr!="&nbsp") else 0
        team2_second_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_p2_score']").text
        team2_second_qtr=team2_second_qtr if(team2_second_qtr!="&nbsp") else 0
        team2_third_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_p3_score']").text
        team2_third_qtr=team2_third_qtr if(team2_third_qtr!="&nbsp") else 0
        team2_fourth_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_p4_score']").text
        team2_fourth_qtr= team2_fourth_qtr if( team2_fourth_qtr!="&nbsp") else 0
        team2_ot_qtr=driver.find_element(By.XPATH,"//span[@id='aj_2_ot_score']").text
        t2_ot=team2_ot_qtr if(team2_ot_qtr!="&nbsp") else 0
        t2_qtr={
            "first":int(team2_first_qtr),
            "second":int(team2_second_qtr),
            "third":int(team2_third_qtr),
            "fourth":int(team2_fourth_qtr), 
            "ot":int(t2_ot) 
        }   """

        female_team=["ULAANBAATAR AMAZONS","УБ АМАЗОНС","OMNI KHULEGUUD","OMNI ХАСЫН ХҮЛЭГҮҮД","AO SCORPIONS","M WINX","STARS","Мон Пон","ARAVT","АРАВТ"]
        team1_name=driver.find_element(By.XPATH,"//div[contains(@class,'team-0-bs')]/div[2]/span").text
        if team1_name in female_team:
            gender=0
        else:
            gender=1 
        team1_common_name=common_name(team1_name)       
        team1_score=int(driver.find_element(By.XPATH,"//div[contains(@class,'team team-0')]/div[5]/span").text)
        team2_name=driver.find_element(By.XPATH,"//div[contains(@class,'team-1-bs')]/div[2]/span").text
        team2_score=int(driver.find_element(By.XPATH,"//div[contains(@class,'team team-1')]/div[5]/span").text)
        team2_common_name=common_name(team2_name)
        if int(team1_score)>int(team2_score):
            t1_win=1
        else: 
            t1_win=0
        t2_win=1-t1_win 
        imp_plr=0   
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
                    player=find_stat(driver,xpath,team1_common_name,1,t1_win)
                    t1_players.append(player)
                    #print(player)
                    #current_game.insert_one(player)
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
                    player1=find_stat(driver,xpath1,team1_common_name,0,t1_win)
                    #print(player1)
                    t1_players.append(player1)
                    #current_game.insert_one(player1)
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
                    player_t2=find_stat(driver,xpath_t2,team2_common_name,1,t2_win)
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
                    player1_t2=find_stat(driver,xpath1_t2,team2_common_name,0,t2_win)
                    #print(player1)
                    t1_players.append(player1_t2)
                    #current_game.insert_one(player1)
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

        driver.quit()
        ######----------------------------------add-to- dictionary----------------------------------------    
        game={
                "_id":   "ongoing",
                "link"       : link_game,
                "t1_name"    : team1_common_name,
                "t1_score"   : team1_score,
                "t2_name"    : team2_common_name,
                "t2_score"   : team2_score,
                "season"     : "post2025",
                "male"       : gender, 
                "date"       : date_obj,    
                "t1_players" : t1_players,
                "team1_stat" : team1_data,
                "team2_stat" : team2_data,
                
                "t1_win"     : t1_win,
                "t2_win"     : t2_win    
                }
            # "t1_qtr"     : t1_qtr,
            # "t2_qtr"     : t2_qtr,
        #game_rec=current_game.find_one({},{_id:1})
        #print(game_rec)
        update_query={'_id':"ongoing"}
        update_operation={'$set':game}
        current_game.update_one(update_query,update_operation)    
        #current_game.insert_one(game)
        return jsonify(game)


@app.route('/player_stat',methods=['GET','POST'])
def pl_stat():
    if request.method=='POST':
        print(request.form.getlist('sel_col'))
        return 'Done'
        
    return render_template('public/base_stat.html')
    
@app.route("/deedleague/update",methods=["GET"])
def data_update():
    if request.args:
        # get arguments
        name1=request.args.get("name1")
        if link_archive.find_one({"link":name1}):
            print("it exists")
        else:
            rec_id=link_archive.insert_one({"link":name1})
            print("added")
        #togloltiin linkiig avch current game-ryy nemne
        add_current(name1)
    return jsonify(name1)

#PLAYER STAT LINKIIG AJILLUULAH HESEG  
@app.route("/shuud")
def shuud_stat():
    plr={}
    h_team=[] # home toglogchdiin stat hadgalna
    a_team=[] # away toglogchdiin stat hadgalna
    #current game database-iin utgiig avna
    plrs=current_game.find_one()
    
    home_team=plrs['t1_name']
    home_short=find_brief(home_team)
    #print(home_short)
    away_team=plrs['t2_name']
    away_short=find_brief(away_team)
    #odoo bolj baigaa togloltoos toglogchdiin stat list-iig yalgaj avna
    lists=plrs['t1_players']
    for lis in lists:
       # for key in lis:
                plr['num']=lis['p_number']
                plr['name']=lis['p_name']
                plr['pts']=lis['p_points']
                plr['fg']=str(lis['fg_made'])+"/"+str(lis['fg_attempt'])
                plr['fg_p']=round(lis['p_fg_percent'],1)
                plr['2p']=str(lis['two_p_made'])+"/"+str(lis['two_p_attempt'])
                plr['2p_p']=round(lis['p_two_p_percent'],1)
                plr['3p']=str(lis['three_p_made'])+"/"+str(lis['three_p_attempt'])
                plr['3p_p']=round(lis['p_three_p_percent'],1)
                plr['ft']=str(lis['ft_made'])+"/"+str(lis['ft_attempt'])
                plr['ft_p']=round(lis['p_ft_percent'],1)
                plr['reb']=lis['p_rebound']
                plr['ast']=lis['p_assist']
                plr['to']=lis['p_turnover']
                plr['stl']=lis['p_steal']
                plr['block']=lis['p_block']
                plr['min_plus']=lis['p_min_plus']
                #Home Team list-d nemne
                if lis['team']==home_team:
                    h_team.append(plr)
                    
                    #utgaa listed nemsenii daraa utgaa teglene
                    plr={}
                #Away Team list-d nemne    
                else :
                    a_team.append(plr)  
                    plr={}
    #add_livestat_name(a_team,away_short)                
    # Debug Purpose
    # print(f"Key: {a_team}")
    #Shuud Stat-iig haruulah JINJA Template huudas duudna
    return render_template('public/shuud_stat.html',home_short=home_short,away_short=away_short,h_team=h_team,a_team=a_team)

# shuud_stat.html-ees ilgeesen home player stat aguulsan json-iig update hiine 
@app.route("/h_plr_stat",methods=["PATCH"])   
def h_update_plr():
    plr_avg={}
    try:
        if request.is_json:
            hooson=0
            req=request.get_json()
            #print(req)
            last_season=["2023","post2023","2024","post2024"]
            this_season=["2025","post2025"]
            plr_num=req.get("plr_num")
            plr_name=req.get("plr_name")
            #Aggregate hesgees dundjiig tootsoh function duudne
            plr_last_stat=avg_plr_stat(plr_name,last_season)
            if len(plr_last_stat)==0:
                hooson=1
            plr_a_stat=avg_plr_stat(plr_name,this_season)
            #print(plr_a_stat['fg'])
            
            s_title1=req.get("stat_title1")
            if s_title1==None:
                s_title1="pts" #default value if nothing is selected
                stat11=plr_a_stat["pts"]
                stat111="" if hooson else plr_last_stat['pts'] 
            else:
                stat11=plr_a_stat[s_title1]  
                stat111="" if hooson else plr_last_stat[s_title1] 
                s_title1=title_name(s_title1)  
            stat1=req.get("stat1")
            
            s_title2=req.get("stat_title2") 
            stat2=req.get("stat2") 
            s_title3=req.get("stat_title3")
            stat3=req.get("stat3") 
            s_title4=req.get("stat_title4")
            stat4=req.get("stat4") 
            s_title5=req.get("stat_title5")
            stat5=req.get("stat5") 
         
            print(plr_last_stat)
            #print(plr_a_stat)
            #print(s_title4)
            #stat Title none bol hooson utga hadgalna
            if s_title2==None :
                s_title2=""
                stat2="" 
                stat22=""
                stat222=""
            else:  
                stat22=plr_a_stat[s_title2]
                stat222="" if hooson else plr_last_stat[s_title2]   #get key value before modifying title is important
                s_title2=title_name(s_title2)
            if s_title3==None :
                s_title3=""
                stat3=""
                stat33=""
                stat333=""
            else:
                stat33=plr_a_stat[s_title3] 
                stat333="" if hooson else plr_last_stat[s_title3]  
                s_title3=title_name(s_title3) 
            
            if s_title4==None :
                s_title4=""
                stat4=""
                stat44=""
                stat444=""
            else:
                stat44=plr_a_stat[s_title4] 
                stat444="" if hooson else plr_last_stat[s_title4] 
                s_title4=title_name(s_title4) 
                     
            if s_title5==None :
                s_title5=""
                stat5=""  
                stat55=""
                stat555=""
            else:
                stat55=plr_a_stat[s_title5] 
                stat555="" if hooson else plr_last_stat[s_title5] 
                s_title5=title_name(s_title5) 
            
            h_plr_stat={
                "home_current_stat":{
                    "h_plr_num":plr_num,
                    "h_plr_name":plr_name,
                    "h_title1":s_title1,
                    "h_title2":s_title2,
                    "h_title3":s_title3,
                    "h_title4":s_title4,
                    "h_title5":s_title5,
                    "h_stat1":stat1,
                    "h_stat2":stat2,
                    "h_stat3":stat3,
                    "h_stat4":stat4,
                    "h_stat5":stat5,
                    "h_avg_stat1":stat11,
                    "h_avg_stat2":stat22,
                    "h_avg_stat3":stat33,
                    "h_avg_stat4":stat44,
                    "h_avg_stat5":stat55,
                    "h_last_season_stat1":stat111,
                    "h_last_season_stat2":stat222,
                    "h_last_season_stat3":stat333,
                    "h_last_season_stat4":stat444,
                    "h_last_season_stat5":stat555
                    }
            }  
            full_id={'_id':"full_stat"} 
            h_plr_current={"$set":h_plr_stat} 
            dbResponse=mystat.update_one(full_id,h_plr_current)
            #mystat.insert_one(h_plr_stat)  
            #print(h_plr_stat)
            
                       
            #for attr in dir(dbResponse):
            #    print(f"***************{attr}")
            return Response(response=json.dumps("{message: home stat updated }"),
            status=200,
            mimetype="application/json"
        )     
    except Exception as ex:
        print("*************")   
        print(ex)
        print("*************") 
        return Response(response=json.dumps("{message:cannot reset}"),
            status=500,
            mimetype="application/json"
        ) 
    
# shuud_stat.html-ees ilgeesen home player stat aguulsan json-iig update hiine 
@app.route("/g_plr_stat",methods=["PATCH"])   
def guest_update_plr():
    try:
        if request.is_json:
            req=request.get_json()
            #print(req)
            hooson=0
            last_season=["2023","post2023","2024","post2024"]
            this_season=["2025","post2025"]
            plr_num=req.get("plr_num")
            plr_name=req.get("plr_name")
            plr_last_stat=avg_plr_stat(plr_name,last_season)
            if len(plr_last_stat)==0:
                hooson=1
            plr_a_stat=avg_plr_stat(plr_name,this_season)
            s_title1=req.get("stat_title1")
            if s_title1==None:
                s_title1="pts" #default value if nothing is selected
                stat11=plr_a_stat["pts"]
                stat111="" if hooson else plr_last_stat['pts'] 
            else:
                stat11=plr_a_stat[s_title1] 
                stat111="" if hooson else plr_last_stat[s_title1] 
                s_title1=title_name(s_title1)  
            stat1=req.get("stat1")
            s_title2=req.get("stat_title2") 
            stat2=req.get("stat2") 
            s_title3=req.get("stat_title3")
            stat3=req.get("stat3") 
            s_title4=req.get("stat_title4")
            stat4=req.get("stat4") 
            s_title5=req.get("stat_title5")
            stat5=req.get("stat5") 
            #stat Title none bol hooson utga hadgalna
            if s_title2==None :
                s_title2=""
                stat2="" 
                stat22=""
                stat222=""
            else:  
                stat22=plr_a_stat[s_title2]
                stat222="" if hooson else plr_last_stat[s_title2]   #get key value before modifying title is important
                s_title2=title_name(s_title2)
            if s_title3==None :
                s_title3=""
                stat3=""
                stat33=""
                stat333=""
            else:
                stat33=plr_a_stat[s_title3] 
                stat333="" if hooson else plr_last_stat[s_title3]  
                s_title3=title_name(s_title3) 
            
            if s_title4==None :
                s_title4=""
                stat4=""
                stat44=""
                stat444=""
            else:
                stat44=plr_a_stat[s_title4] 
                stat444="" if hooson else plr_last_stat[s_title4] 
                s_title4=title_name(s_title4) 
                     
            if s_title5==None :
                s_title5=""
                stat5=""  
                stat55=""
                stat555=""
            else:
                stat55=plr_a_stat[s_title5] 
                stat555="" if hooson else plr_last_stat[s_title5]  
                s_title5=title_name(s_title5) 
            g_plr_stat={
                "guest_current_stat":{
                    "g_plr_num":plr_num,
                    "g_plr_name":plr_name,
                    "g_title1":s_title1,
                    "g_title2":s_title2,
                    "g_title3":s_title3,
                    "g_title4":s_title4,
                    "g_title5":s_title5,
                    "g_stat1":stat1,
                    "g_stat2":stat2,
                    "g_stat3":stat3,
                    "g_stat4":stat4,
                    "g_stat5":stat5,
                    "g_avg_stat1":stat11,
                    "g_avg_stat2":stat22,
                    "g_avg_stat3":stat33,
                    "g_avg_stat4":stat44,
                    "g_avg_stat5":stat55,
                    "g_last_season_stat1":stat111,
                    "g_last_season_stat2":stat222,
                    "g_last_season_stat3":stat333,
                    "g_last_season_stat4":stat444,
                    "g_last_season_stat5":stat555}
            }  
            full_id={'_id':"full_stat"} 
            g_plr_current={"$set":g_plr_stat} 
            dbResponse=mystat.update_one(full_id,g_plr_current)
            #mystat.insert_one(h_plr_stat)  
            print(g_plr_stat)
            
                       
            #for attr in dir(dbResponse):
            #    print(f"***************{attr}")
            return Response(response=json.dumps("{message: home stat updated }"),
            status=200,
            mimetype="application/json"
        )     
    except Exception as ex:
        print("*************")   
        print(ex)
        print("*************") 
        return Response(response=json.dumps("{message:cannot reset}"),
            status=500,
            mimetype="application/json"
        ) 


# Live Team stat route hiih heseg    
@app.route("/team_stat")   
def h_update_team():
    #current game database-iin utgiig avna
    home_stat={}
    away_stat={}
    teams=current_game.find_one() 
    ht_stat=teams["team1_stat"]
    at_stat=teams["team2_stat"]
    # Remap and Joins some data
    home_stat['name']=find_brief(teams['t1_name'])
    home_stat['pts']=ht_stat['t_points']
    home_stat['fg']=str(ht_stat['t_fg_made'])+"/"+str(ht_stat['t_fg_attempt'])
    home_stat['fgp']=round(ht_stat['t_fg_percent'],1)
    home_stat['2p']=str(ht_stat['t_two_p_made'])+"/"+str(ht_stat['t_two_p_attempt'])
    home_stat['2pp']=round(ht_stat['t_two_p_percent'],1)
    home_stat['3p']=str(ht_stat['t_three_made'])+"/"+str(ht_stat['t_three_attempt'])
    home_stat['3pp']=round(ht_stat['t_three_p_percent'],1)
    home_stat['ft']=str(ht_stat['t_ft_made'])+"/"+str(ht_stat['t_ft_attempt'])
    home_stat['ftp']=round(ht_stat['t_ft_percent'],1)
    home_stat['o/reb']=ht_stat['t_offensive']
    home_stat['d/reb']=ht_stat['t_defensive']
    home_stat['reb']=ht_stat['t_rebound']
    home_stat['ast']=ht_stat['t_assist']
    home_stat['to']=ht_stat['t_turnover']
    home_stat['stl']=ht_stat['t_steal']
    home_stat['blck']=ht_stat['t_block']
    home_stat['foul']=ht_stat['t_foul']
    home_stat['pts_f_to']=ht_stat['pts_f_to']
    home_stat['pts_paint']=ht_stat['pts_paint']
    home_stat['sec_c_pt']=ht_stat['two_c_p']
    home_stat['pts_fast']=ht_stat['pts_fast']
    home_stat['pts_bench']=ht_stat['pts_bench']
    home_stat['lead']=ht_stat['lead']
    home_stat['score_run']=ht_stat['score_run']
    

    away_stat['name']=find_brief(teams['t2_name'])
    away_stat['pts']=at_stat['t_points']
    away_stat['fg']=str(at_stat['t_fg_made'])+"/"+str(at_stat['t_fg_attempt'])
    away_stat['fgp']=round(at_stat['t_fg_percent'],1)
    away_stat['2p']=str(at_stat['t_two_p_made'])+"/"+str(at_stat['t_two_p_attempt'])
    away_stat['2pp']=round(at_stat['t_two_p_percent'],1)
    away_stat['3p']=str(at_stat['t_three_made'])+"/"+str(at_stat['t_three_attempt'])
    away_stat['3pp']=round(at_stat['t_three_p_percent'],1)
    away_stat['ft']=str(at_stat['t_ft_made'])+"/"+str(at_stat['t_ft_attempt'])
    away_stat['ftp']=round(at_stat['t_ft_percent'],1)
    away_stat['o/reb']=at_stat['t_offensive']
    away_stat['d/reb']=at_stat['t_defensive']
    away_stat['reb']=at_stat['t_rebound']
    away_stat['ast']=at_stat['t_assist']
    away_stat['to']=at_stat['t_turnover']
    away_stat['stl']=at_stat['t_steal']
    away_stat['blck']=at_stat['t_block']
    away_stat['foul']=at_stat['t_foul']
    away_stat['pts_f_to']=at_stat['pts_f_to']
    away_stat['pts_paint']=at_stat['pts_paint']
    away_stat['sec_c_pt']=at_stat['two_c_p']
    away_stat['pts_fast']=at_stat['pts_fast']
    away_stat['pts_bench']=at_stat['pts_bench']
    away_stat['lead']=at_stat['lead']
    away_stat['score_run']=at_stat['score_run']
    #away_stat['last_plays']=last_games(teams['t2_name'],7)
    home_last7=last_games(teams['t1_name'],7)
    away_last7=last_games(teams['t2_name'],7) 
    print(away_last7)
    last_sev=[]
    last_sev.append(home_last7)
    last_sev.append(away_last7)
    team_full_stat={
        "team_full_stat":{
            "home_full":home_stat,
            "away_full":away_stat,
            "last7":last_sev
             }}
    
    full_id={'_id':"full_stat"} 
    team_full_current={"$set":team_full_stat} 
    dbResponse=mystat.update_one(full_id,team_full_current)

    return render_template('public/shuud_teams.html',home_stat=home_stat,away_stat=away_stat)     

# shuud_teams.html-ees ilgeesen songogdson team stat (maximum 5) byhii json-iig update hiine 
@app.route("/team_update_stat",methods=["PATCH"])   
def update_team():
    try:
        if request.is_json:
            req=request.get_json()
            #print(req) # debug for testing request
            s_title1=req.get("stat_title1")
            ht_stat1=req.get("ht_stat1")
            gt_stat1=req.get("gt_stat1")
            s_title2=req.get("stat_title2") 
            ht_stat2=req.get("ht_stat2")
            gt_stat2=req.get("gt_stat2")
            s_title3=req.get("stat_title3")
            ht_stat3=req.get("ht_stat3") 
            gt_stat3=req.get("gt_stat3")
            s_title4=req.get("stat_title4")
            ht_stat4=req.get("ht_stat4") 
            gt_stat4=req.get("gt_stat4")
            s_title5=req.get("stat_title5")
            ht_stat5=req.get("ht_stat5")
            gt_stat5=req.get("gt_stat5") 
            #stat Title none bol hooson utga hadgalna
            if s_title2==None :
                s_title2=""
                ht_stat2=""
                gt_stat2=""
            if s_title3==None :
                s_title3=""
                ht_stat3=""
                gt_stat3=""
            if s_title4==None :
                s_title4=""
                ht_stat4=""
                gt_stat4=""   
            if s_title5==None :
                s_title5=""
                ht_stat5=""
                gt_stat5=""
            cur_team_stat={
                "team_current_stat":{
                    "title1":s_title1,
                    "title2":s_title2,
                    "title3":s_title3,
                    "title4":s_title4,
                    "title5":s_title5,
                    "ht_stat1":ht_stat1,
                    "ht_stat2":ht_stat2,
                    "ht_stat3":ht_stat3,
                    "ht_stat4":ht_stat4,
                    "ht_stat5":ht_stat5,
                    "gt_stat1":gt_stat1,
                    "gt_stat2":gt_stat2,
                    "gt_stat3":gt_stat3,
                    "gt_stat4":gt_stat4,
                    "gt_stat5":gt_stat5}
            }  
            full_id={'_id':"full_stat"} 
            h_plr_current={"$set":cur_team_stat} 
            dbResponse=mystat.update_one(full_id,h_plr_current)
            #mystat.insert_one(h_plr_stat)  
            print(cur_team_stat)
            
                       
            #for attr in dir(dbResponse):
            #    print(f"***************{attr}")
            return Response(response=json.dumps("{message: home stat updated }"),
            status=200,
            mimetype="application/json"
        )     
    except Exception as ex:
        print("*************")   
        print(ex)
        print("*************") 
        return Response(response=json.dumps("{message:cannot reset}"),
            status=500,
            mimetype="application/json"
        ) 
@app.route("/plr_avg")
def sum_avg():
    #Odoo bolj baigaa togloltiin database-aas home,away bagiin short neriig avna
    home_names=[]
    away_names=[]
    cur_game=mystat.find_one()
    h_short=cur_game['team_full_stat']['home_full']['h_short_name']
    a_short=cur_game['team_full_stat']['away_full']['a_short_name']
    #Bagiin Short nerend hargalzah toglogchdiin nersiig roster-oos avna 
    h_cursor=roster.find_one({"TeamShort":h_short})
    a_cursor=roster.find_one({"TeamShort":a_short})
    h_plrs=h_cursor['players']
    a_plrs=a_cursor['players']
    for ii in h_plrs:
        home_names.append(ii['Firstname'])
    for jj in a_plrs:
        away_names.append(jj['Firstname'])

    print(home_names)
    print(away_names)
    print(f"{h_short} and {a_short}")
    return render_template("public/player_average.html",h_short=h_short,a_short=a_short,home_names=home_names,away_names=away_names)

def add_livestat_name(team_list,short_name):
    dd=roster.find_one({"TeamShort":short_name}) 
    #for h_p in dd:
    home_list=dd['players']
    #print(home_list)
    for each in home_list:
        print(each['Firstname'])  
        number=each['PlayerNumber']
        print(each['PlayerNumber']) 
        for every in team_list:
            if number==str(every['num']):
                #field=short_name+".players.$[element]"
                roster.update_one({"TeamShort":short_name,"players.PlayerNumber":str(every['num'])},{"$set":{"players.$.ls_name":every['name']}},upsert=True)
                print(every['name'])
    return 1    

@app.route("/stats_deed")
def throw_stat():
    stats={}
    respond=mystat.find({})
    for sts in respond:
        stats["stats"]=sts
        print(sts)
    return Response(response=json.dumps(stats,ensure_ascii = False),
              status=200,
              mimetype="application/json")    

#Full stat shinechleh holboosuud
def update_team_stats():
    return redirect("/team_stat", code=302)   
def update_home_plr_stats():
    return redirect("/h_plr_stat", code=302)   
def update_guest_plr_stats():
    return redirect("/g_plr_stat", code=302)  
def update_chosen_team():
    return redirect("/team_update_stat", code=302)   

#Xpression-ees duudahad livestat shichlene  
@app.route("/halfs")  
def update_cur_game():
    #Update current game link automatic
    teams=current_game.find_one()    
    link=teams['link']
    add_current(link)
    """update_team_stats()
    update_home_plr_stats()
    update_guest_plr_stats()
    update_chosen_team()"""
    return redirect("/team_stat", code=302)  
    return Response(response=json.dumps("{message: home stat updated }"),
            status=200,
            mimetype="application/json"
        )     
