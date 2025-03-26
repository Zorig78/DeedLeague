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
from .my_functions import find_stat,find_team_stat ,find_brief,common_name,find_list_value
from .my_functions import *
from .aggregate import avg_plr_stat,last_games
from .aggregate2 import *

last_season=["2023","post2023","2024","post2024"]
this_season=["2025","post2025"]

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

client=pymongo.MongoClient()
mydb = client["DeedLeague"] 
games_col=mydb["Games"]
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
@app.route("/compare",methods=["GET","POST"])
def compare():
    team_names={"БМ":"БИШРЭЛТ МЕТАЛЛ","ЭТМ":"ЭРДЭНЭТ MINERS","ТЛЖ":"INUT YES TLG","ХХ":"ХАСЫН ХҮЛЭГҮҮД", 
                "ШГА":"SG APES","БРО":"ЗАВХАН BROTHERS","СЭЛ":"СЭЛЭНГЭ БОДОНС","ДЮ":"DARKHAN UNITED","БСЭ":"BCH KNIGHTS","НАЛ":"НАЛАЙХ BISON"}
    if request.method=='POST':
        print(request.form.getlist('sel_col'))
        return 'Done'
        
    return render_template('public/Select2team.html',team_names=team_names)

@app.route("/vs_stat",methods=["PATCH"])   
def vs_update():
    try:
        if request.is_json:
            req=request.get_json()
           
            home_team=req.get("team1")
            guest_team=req.get("team2")
            num_of_games=int(req.get("game_num"))
                       
            h_tm_stat=two_team_meeting(home_team,guest_team,num_of_games)  
            a_tm_stat=two_team_meeting(guest_team,home_team,num_of_games)   
            if len(h_tm_stat):
                home_avg_stat=h_tm_stat[-1]
                h_tm_stat.pop(-1)
                print(h_tm_stat)
                print(home_avg_stat)
                print(a_tm_stat[-1])    
                print(get_title("avg_points"))                  
            return Response(response=json.dumps("{message: vs stat updated }"),
            status=200,
            mimetype="application/json" )
    except Exception as ex:
        print("*************")   
        print(ex)
        print("*************") 
        return Response(response=json.dumps("{message:cannot update vs stat}"),
            status=500,
            mimetype="application/json"
        )      
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

# shuud_stat.html-ees ilgeesen home player stat aguulsan json-iig avch database-d update hiine 
@app.route("/h_plr_stat",methods=["PATCH"])   
def h_update_plr():
    try:
        if request.is_json:
            req=request.get_json()
            titles=[]
            stats=[]
            plr_num=req.get("plr_num")
            plr_name=req.get("plr_name")
            #Aggregate hesgees ongorson bolon ene season-ii dundjiig tootsoh function duudne
            plr_last_stat=avg_plr_stat(plr_name,last_season)
            plr_a_stat=avg_plr_stat(plr_name,this_season)
            for i in range(1,6):
                titles.append(req.get("stat_title"+str(i)))
                stats.append(req.get("stat"+str(i)))
             
            
            result=find_list_value(titles,stats,plr_a_stat,plr_last_stat)
            
            plr_stat=assign_stat_to_dic(plr_num,plr_name,result)   
            home_plr_stat={"h_plr_stat":plr_stat}                  
           
            full_id={'_id':"full_stat"} 
            h_plr_current={"$set":home_plr_stat} 
            dbResponse=mystat.update_one(full_id,h_plr_current)
                      
            return Response(response=json.dumps("{message: home player stat updated }"),
            status=200,
            mimetype="application/json" )     
    except Exception as ex:
        print("*************")   
        print(ex)
        print("*************") 
        return Response(response=json.dumps("{message:cannot update player stat}"),
            status=500,
            mimetype="application/json"
        ) 

    
# shuud_stat.html-ees ilgeesen home player stat aguulsan json-iig update hiine 
@app.route("/g_plr_stat",methods=["PATCH"])   
def guest_update_plr():
    try:
        if request.is_json:
            req=request.get_json()
            titles=[]
            stats=[]
            plr_num=req.get("plr_num")
            plr_name=req.get("plr_name")
            plr_last_stat=avg_plr_stat(plr_name,last_season)
            plr_a_stat=avg_plr_stat(plr_name,this_season)
            for i in range(1,6):
                titles.append(req.get("stat_title"+str(i)))
                stats.append(req.get("stat"+str(i)))
            result=find_list_value(titles,stats,plr_a_stat,plr_last_stat)
            
            plr_stat=assign_stat_to_dic(plr_num,plr_name,result)   
            guest_plr_stat={"g_plr_stat":plr_stat}                  
           
            full_id={'_id':"full_stat"} 
            g_plr_current={"$set":guest_plr_stat} 
            dbResponse=mystat.update_one(full_id,g_plr_current)
            print(guest_plr_stat)
                                
            return Response(response=json.dumps("{message: guest player stat updated }"),
            status=200,
            mimetype="application/json" )     
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
    #---------assign home team stat to dictionary
    ht_stat=teams["team1_stat"]
    ht_name=teams["t1_name"]
    home_stat=assign_team_stat_to_dict(ht_stat,ht_name)
    at_stat=teams["team2_stat"]
    at_name=teams["t2_name"]
    away_stat=assign_team_stat_to_dict(at_stat,at_name)
    #away_stat['last_plays']=last_games(teams['t2_name'],7)
    home_last7=last_games(teams['t1_name'],7)
    away_last7=last_games(teams['t2_name'],7) 
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
            titles=[]
            ht_stats=[]
            ht_season_avg={}
            ht_prev_avg={}
            gt_season_avg={}
            gt_prev_avg={}
            gt_stats=[]
            key_title=[]
            req=request.get_json()
            print(req) # debug for testing request
            #-------get home and guest team names from current game database 
            curs=current_game.find_one()
            hteam=curs['t1_name']
            gteam=curs['t2_name']
            for i in range(1,6):
                titles.append(req.get("stat_title"+str(i)))
                ht_stats.append(req.get("ht_stat"+str(i)))
                gt_stats.append(req.get("gt_stat"+str(i)))
            for tt in titles:
                if tt!=None:
                    key_title.append(rev_title(tt))
                else:
                    key_title.append(None) 
            for index,value in enumerate(key_title):
                if value!=None:
                    ht_fnd=team_avg_stat(this_season,hteam,value) 
                    ht_fnd1=team_avg_stat(last_season,hteam,value) 
                    gt_fnd=team_avg_stat(this_season,gteam,value) 
                    gt_fnd1=team_avg_stat(last_season,gteam,value) 
                    ht_season_avg[titles[index]]=(ht_fnd['sts'])  
                    ht_prev_avg[titles[index]]=(ht_fnd1['sts'])    
                    gt_season_avg[titles[index]]=(gt_fnd['sts'])  
                    gt_prev_avg[titles[index]]=(gt_fnd1['sts'])   
            h_res=find_list_value(titles,ht_stats,ht_season_avg,ht_prev_avg)
            g_res=find_list_value(titles,gt_stats,gt_season_avg,gt_prev_avg) 
            home_stat_dict=assign_stat_to_dic("",hteam,h_res)
            guest_stat_dict=assign_stat_to_dic("",gteam,g_res)
            home_stat_dict.pop('plr_num')
            home_stat_dict['ht_name']=home_stat_dict.pop('plr_name')
            home_stat_dict['h_short']=find_brief(hteam)
            guest_stat_dict['gt_name']=guest_stat_dict.pop('plr_name')
            guest_stat_dict['g_short']=find_brief(gteam)
            guest_stat_dict.pop('plr_num')
            print(home_stat_dict)
            print(guest_stat_dict)              
                 
                
            
            cur_team_stat={
                "cur_game_team_stat":{
                    "home_team":home_stat_dict,
                    "guest_team":guest_stat_dict,
                    }
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
