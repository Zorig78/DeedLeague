from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select;
from selenium.common.exceptions import TimeoutException
import time
from flask import render_template, request, redirect,jsonify
from datetime import datetime
import pandas as pd
import csv
from selenium.webdriver.support.color import Color
from selenium.common.exceptions import NoSuchElementException
import pymongo
import pprint
from .links import import25

client=pymongo.MongoClient()
mydb = client["DeedLeague"] 
current_game=mydb['current_game']

teams25_male=["БИШРЭЛТ МЕТАЛЛ","ЭРДЭНЭТ MINERS","INUT YES TLG","ХАСЫН ХҮЛЭГҮҮД","SG APES","ЗАВХАН BROTHERS","СЭЛЭНГЭ БОДОНС","BCH KNIGHTS","DARKHAN UNITED","НАЛАЙХ BISON"]
team_stat=["t_points","t_fg_percent","t_two_p_percent","t_three_p_percent","t_ft_percent","t_offensive","t_defensive","t_rebound","t_assist","t_turnover",
           "t_steal","t_block","t_foul","pts_f_to","pts_paint","two_c_p","pts_fast","pts_bench"]
global plr_stat,common_team_name
# assign appropriate title to the matching stat 
def get_title(tit):
    match_list=['date','t1_ner','avg_points','avg_fg_percent','avg_two_p_percent','avg_three_p_percent','avg_ft_percent',
                'avg_offensive','avg_defensive','avg_rebound','avg_assist','avg_turnover','avg_steal','avg_block','avg_foul',
                 'avg_pts_f_to','avg_pts_paint','avg_two_c_p','avg_pts_fast','avg_pts_bench',
                 #player titles
                 'pts','fg','fgp','2p','2pp','3p','3pp','ft','ftp','reb','ast','to','stl','blck','pl_min',
                 #team_related
                 'off_reb','def_reb','foul','p_f_to','p_paint','sec_chance','fast','bench','lead','run']
    title_list=['Он сар','Нэр','Оноо','Довт %','2 оноо %','3 оноо %','Ч/шид %','Д/сам','Х/сам','Сам','Дамж','Б/алд',
                'Тас','Хаалт','Алд','Б/а/оноо','Буд/тал','2/Бол','Хур/дов','Сэл',
                'Оноо','Дов','Дов%','2Pt','2Pt%','3pt','3pt%','Ч/шид','Ч/шид%','Сам','Дам','Б/алд','Тас','Хаалт','+/-',
                'Х/сам','Д/сам','Алд','Б/а/оноо','Буд/тал','2/Бол','Хур/дов','Сэл','lead','run']
   
    title_dict=dict(zip(match_list,title_list))
    if tit=="":
        title=""
        return title
    return title_dict[tit]
# convert chosen title to database json key
def rev_title(ti_name):
    tit_list=['pts','fg','fgp','2p','2pp','3p','3pp','ft','ftp','off_reb','def_reb','reb','ast','to',
                'stl','blck','foul','p_f_to','p_paint','sec_chance','fast','bench']
    mat_list=["t_points","t_fg","t_fg_percent","t_2p","t_two_p_percent","t_three","t_three_p_percent","t_ft","t_ft_percent"
              ,"t_offensive","t_defensive","t_rebound","t_assist","t_turnover","t_steal","t_block","t_foul","pts_f_to",
              "pts_paint","two_c_p","pts_fast","pts_bench"]
    rev_dict=dict(zip(tit_list,mat_list))
    if ti_name=="":
        title=""
        return title
    return rev_dict[ti_name]
 
 

def common_name(t_name):
    if t_name in ["ULAANBAATAR AMAZONS","УБ АМАЗОНС"]:
        common_team_name="УБ АМАЗОНС"
    elif t_name in ["OMNI KHULEGUUD","OMNI ХАСЫН ХҮЛЭГҮҮД"]:
        common_team_name="ОМНИ ХҮЛЭГҮҮД"
    elif t_name in ["БИШРЭЛТ МЕТАЛЛ","BISHRELT METALL","ТЭНҮҮН ӨЛЗИЙ МЕТАЛЛ"]:
        common_team_name="БИШРЭЛТ МЕТАЛЛ"
    elif t_name in ["ЭРДЭНЭТИЙН УУРХАЙЧИД","ERDENET MINERS","ЭРДЭНЭТ MINERS"]:
        common_team_name="ЭРДЭНЭТ MINERS" 
    elif t_name in ["ULAANBAATAR TLG","UB TLG","ULAANBAATAR TLG","TLG ONDILT","INUT YES TLG"]:
        common_team_name="INUT YES TLG"  
    elif t_name in ["KHULEGUUD","ХАСЫН ХҮЛЭГҮҮД"]:
        common_team_name="ХАСЫН ХҮЛЭГҮҮД"    
    elif t_name in ["IHC APES","SG APES"]:
        common_team_name="SG APES"   
    elif t_name in ["ZAVKHAN BROTHERS","ЗАВХАН BROTHERS"]:
        common_team_name="ЗАВХАН BROTHERS"  
    elif t_name in ["SELENGE BODONS","СЭЛЭНГЭ БОДОНС"]:
        common_team_name="СЭЛЭНГЭ БОДОНС"     
    else: 
        common_team_name=t_name        
    return common_team_name
    

def find_brief(name):
    global result
    if name in ["ULAANBAATAR AMAZONS","УБ АМАЗОНС"]:
        result="АМЗ" 
    elif name in ["KHULEGUUD","ХАСЫН ХҮЛЭГҮҮД"]:
        result="ХҮЛ"
    elif name in ["ЭРДЭНЭТИЙН УУРХАЙЧИД","ERDENET MINERS","ЭРДЭНЭТ MINERS"]:
        result="ЭТМ"  
    elif name in ["БИШРЭЛТ МЕТАЛЛ","BISHRELT METALL","ТЭНҮҮН ӨЛЗИЙ МЕТАЛЛ"]:
        result="БМ"        
    elif name in ["ULAANBAATAR TLG","UB TLG","ULAANBAATAR TLG","TLG ONDILT","INUT YES TLG"]:
        result="ТЛЖ" 
    elif name in ["IHC APES","SG APES","SG АПЕС"]:
        result="ШГА" 
    elif name in ["ZAVKHAN BROTHERS","ЗАВХАН BROTHERS"]:
        result="БРО"  
    elif name in ["НАЛАЙХ BISON","NALAIKH BISON"]:
        result="БИЗ" 
    elif name in ["BCH KNIGHTS"]:
        result="БСЭ"    
    elif name in ["DARKHAN UNITED"]:
        result="ДЮ" 
    elif name in ["SELENGE BODONS","СЭЛЭНГЭ БОДОНС"]:
        result="СЭЛ"                      
    
    return result 
def add_current(link_game): 
      
        #PATH="C:\Program Files\chromedriver.exe"
       
        driver=webdriver.Chrome()
        driver.maximize_window()
       
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

def find_stat(driver,xipath,team1_name,starter,win):
    
    sel_row=driver.find_element(By.XPATH,xipath)
    if(sel_row.get_attribute("class"))!="player-row row-not-used":
        #print(sel_row.get_attribute("class"))
        number=sel_row.find_element(By.XPATH,".//td[1]/span").text
        name=sel_row.find_element(By.XPATH,".//td[2]/a/span").text
        if name in import25:
            imp_plr=1
        else:
            imp_plr=0        
        pos=sel_row.find_element(By.XPATH,".//td[3]/span").text
        minutes=sel_row.find_element(By.XPATH,".//td[5]/span").text
        points=sel_row.find_element(By.XPATH,".//td[6]/span").text
        field_goal=sel_row.find_element(By.XPATH,".//td[7]/span[1]").text+"-"+sel_row.find_element(By.XPATH,".//td[7]/span[2]").text
        #fg_percent=sel_row.find_element(By.XPATH,".//td[8]/span").text
        two_p=sel_row.find_element(By.XPATH,".//td[9]/span[1]").text+"-"+sel_row.find_element(By.XPATH,".//td[9]/span[2]").text
        #two_p_percent=sel_row.find_element(By.XPATH,".//td[10]/span").text
        three_p=sel_row.find_element(By.XPATH,".//td[11]/span[1]").text+"-"+sel_row.find_element(By.XPATH,".//td[11]/span[2]").text
        #three_p_percent=sel_row.find_element(By.XPATH,".//td[12]/span").text
        ft=sel_row.find_element(By.XPATH,".//td[13]/span[1]").text+"-"+sel_row.find_element(By.XPATH,".//td[13]/span[2]").text
        #ft_percent=sel_row.find_element(By.XPATH,".//td[14]/span").text
        offensive=sel_row.find_element(By.XPATH,".//td[15]/span").text
        defensive=sel_row.find_element(By.XPATH,".//td[16]/span").text
        rebound=sel_row.find_element(By.XPATH,".//td[17]/span").text
        assist=sel_row.find_element(By.XPATH,".//td[18]/span").text
        turnover=sel_row.find_element(By.XPATH,".//td[19]/span").text
        steal=sel_row.find_element(By.XPATH,".//td[20]/span").text
        block=sel_row.find_element(By.XPATH,".//td[21]/span").text
        blocker_hold=sel_row.find_element(By.XPATH,".//td[22]/span").text
        blocker=0 if(blocker_hold=="") else blocker_hold
        p_foul_holder=sel_row.find_element(By.XPATH,".//td[23]/span").text
        p_foul=0 if(p_foul_holder=="") else p_foul_holder
        fouls_on_holder=sel_row.find_element(By.XPATH,".//td[24]/span").text
        fouls_on=0 if(fouls_on_holder=="") else fouls_on_holder
        min_plus_holder=sel_row.find_element(By.XPATH,".//td[25]/span").text
        min_plus=0 if(min_plus_holder=="") else min_plus_holder

        #print(number+"\n"+name+"\n"+pos+"\n"+minutes+"\n"+points+"\n"+field_goal+"\n"+two_p+"\n"+two_p_percent
        #        +"\n"+ft+"\n"+ft_percent+"\n"+offensive+"\n"+defensive+"\n"+rebound+"\n"+assist+"\n"+turnover+"\n"+steal+"\n"+block+"\n"+min_plus)
        #for child in number:
        #    print(child.get_attribute('innerHTML'))
        #    child.get_attribute('innerHTML')
        sep_time=minutes.split(":")
        total_seconds=int(sep_time[0])*60+int(sep_time[1])
        played=1 if(total_seconds>0.04) else 0
        fg_list=field_goal.split("-")
        fg_percent=round(float(fg_list[0])/float(fg_list[1])*100,2) if(fg_list[1]!="0") else 0
        two_p_list=two_p.split("-")
        two_p_percent=round(float(two_p_list[0])/float(two_p_list[1])*100,2) if(two_p_list[1]!="0") else 0
        three_p_list=three_p.split("-")
        three_p_percent=round(float(three_p_list[0])/float(three_p_list[1])*100,2) if(three_p_list[1]!="0") else 0
        free_th_list=ft.split("-")
        ft_percent=round(float(free_th_list[0])/float(free_th_list[1])*100,2) if(free_th_list[1]!="0") else 0 
        plr_stat={
            "p_number":int(number),
            "p_name":name,
            "p_pos":pos,
            "p_status": played,
            "p_minutes":int(sep_time[0]),
            "p_seconds":int(sep_time[1]),
            "p_totals":total_seconds,
            "p_points":int(points),
            "fg_made":int(fg_list[0]),
            "fg_attempt":int(fg_list[1]),
            "p_fg_percent":float(fg_percent),
            "two_p_made":int(two_p_list[0]),
            "two_p_attempt":int(two_p_list[1]),
            "p_two_p_percent":float(two_p_percent),
            "three_p_made":int(three_p_list[0]),
            "three_p_attempt":int(three_p_list[1]),
            "p_three_p_percent":float(three_p_percent),
            "ft_made":int(free_th_list[0]),
            "ft_attempt":int(free_th_list[1]),
            "p_ft_percent":float(ft_percent),
            "p_offensive":int(offensive),
            "p_defensive":int(defensive),
            "p_rebound":int(rebound),
            "p_assist":int(assist),
            "p_turnover":int(turnover),
            "p_steal":int(steal),
            "p_block":int(block),
            "p_blocker":int(blocker),
            "p_p_foul":int(p_foul),
            "p_fouls_on":int(fouls_on),
            "p_min_plus":float(min_plus),
            "team":team1_name,
            "starter":starter,
            "import":imp_plr,
            "win":win}
    return plr_stat   


def find_team_stat(driver,xipath,stat_path):
    
    sel_row=driver.find_element(By.XPATH,xipath)
    
    #print(sel_row.get_attribute("class"))
    points=sel_row.find_element(By.XPATH,".//td[6]/span").text
    field_goal=sel_row.find_element(By.XPATH,".//td[7]/span[1]").text+"-"+sel_row.find_element(By.XPATH,".//td[7]/span[2]").text
    fg_percent=sel_row.find_element(By.XPATH,".//td[8]/span").text
    two_p=sel_row.find_element(By.XPATH,".//td[9]/span[1]").text+"-"+sel_row.find_element(By.XPATH,".//td[9]/span[2]").text
    two_p_percent=sel_row.find_element(By.XPATH,".//td[10]/span").text
    three_p=sel_row.find_element(By.XPATH,".//td[11]/span[1]").text+"-"+sel_row.find_element(By.XPATH,".//td[11]/span[2]").text
    three_p_percent=sel_row.find_element(By.XPATH,".//td[12]/span").text
    ft=sel_row.find_element(By.XPATH,".//td[13]/span[1]").text+"-"+sel_row.find_element(By.XPATH,".//td[13]/span[2]").text
    ft_percent=sel_row.find_element(By.XPATH,".//td[14]/span").text
    offensive=sel_row.find_element(By.XPATH,".//td[15]/span").text
    defensive=sel_row.find_element(By.XPATH,".//td[16]/span").text
    rebound=sel_row.find_element(By.XPATH,".//td[17]/span").text
    assist=sel_row.find_element(By.XPATH,".//td[18]/span").text
    turnover=sel_row.find_element(By.XPATH,".//td[19]/span").text
    steal=sel_row.find_element(By.XPATH,".//td[20]/span").text
    block=sel_row.find_element(By.XPATH,".//td[21]/span").text
    blocker_holder=sel_row.find_element(By.XPATH,".//td[22]/span").text
    blocker=blocker_holder if(blocker_holder!="") else 0
    p_foul_holder=sel_row.find_element(By.XPATH,".//td[23]/span").text
    p_foul=p_foul_holder if(p_foul_holder!="") else 0
    fouls_on_holder=sel_row.find_element(By.XPATH,".//td[24]/span").text
    fouls_on=fouls_on_holder if(fouls_on_holder!="") else 0
    #min_plus=sel_row.find_element(By.XPATH,".//td[25]/span").text

    team_row=driver.find_element(By.XPATH,stat_path)
    pts_f_to=team_row.find_element(By.XPATH,".//div[2]/span[2]").text 
    pts_paint=team_row.find_element(By.XPATH,".//div[3]/span[2]").text
    two_c_p=team_row.find_element(By.XPATH,".//div[4]/span[2]").text
    pts_fast=team_row.find_element(By.XPATH,".//div[5]/span[2]").text
    pts_bench=team_row.find_element(By.XPATH,".//div[6]/span[2]").text
    lead=team_row.find_element(By.XPATH,".//div[7]/span[2]").text
    score_run=team_row.find_element(By.XPATH,".//div[8]/span[2]").text

    pts_f_to=pts_f_to if(pts_f_to!="") else "0"
    pts_paint=pts_paint if(pts_paint!="") else "0"
    two_c_p=two_c_p if( two_c_p!="") else "0"
    pts_fast=pts_fast if(pts_fast!="") else "0"
    pts_bench=pts_bench if(pts_bench!="") else "0"
    lead=lead if(lead!="") else "0"
    score_run=score_run if(score_run!="") else "0"

    
    fg_list=field_goal.split("-")
    t_fg_percent=round(float(fg_list[0])/float(fg_list[1])*100,2) if(fg_list[1]!="0") else 0
    two_p_list=two_p.split("-")
    t_two_p_percent=round(float(two_p_list[0])/float(two_p_list[1])*100,2) if(two_p_list[1]!="0") else 0
    three_p_list=three_p.split("-")
    t_three_p_percent=round(float(three_p_list[0])/float(three_p_list[1])*100,2) if(three_p_list[1]!="0") else 0
    free_th_list=ft.split("-")
    t_ft_percent=round(float(free_th_list[0])/float(free_th_list[1])*100,2) if(free_th_list[1]!="0") else 0 

    #print(number+"\n"+name+"\n"+pos+"\n"+minutes+"\n"+points+"\n"+field_goal+"\n"+two_p+"\n"+two_p_percent
    #        +"\n"+ft+"\n"+ft_percent+"\n"+offensive+"\n"+defensive+"\n"+rebound+"\n"+assist+"\n"+turnover+"\n"+steal+"\n"+block+"\n"+min_plus)
    #for child in number:
    #    print(child.get_attribute('innerHTML'))
    #    child.get_attribute('innerHTML')
    team_stat={
        "t_points":int(points),
        "t_fg_made":int(fg_list[0]),
        "t_fg_attempt":int(fg_list[1]),
        "t_fg_percent":float(t_fg_percent),
        "t_two_p_made":int(two_p_list[0]),
        "t_two_p_attempt":int(two_p_list[1]),
        "t_two_p_percent":float(t_two_p_percent),
        "t_three_made":int(three_p_list[0]),
        "t_three_attempt":int(three_p_list[1]),
        "t_three_p_percent":float(t_three_p_percent),
        "t_ft_made":int(free_th_list[0]),
        "t_ft_attempt":int(free_th_list[1]),
        "t_ft_percent":float(t_ft_percent),
        "t_offensive":int(offensive),
        "t_defensive":int(defensive),
        "t_rebound":int(rebound),
        "t_assist":int(assist),
        "t_turnover":int(turnover),
        "t_steal":int(steal),
        "t_block":int(block),
        "t_blocker":int(blocker),
        "t_foul":int(p_foul),
        "t_fouls_on":int(fouls_on),
        "pts_f_to":int(pts_f_to),
        "pts_paint":int(pts_paint),
        "two_c_p":int(two_c_p),
        "pts_fast": int(pts_fast),
        "pts_bench":int(pts_bench),
        "lead":int(lead),
        "score_run":int(score_run)}
        #"p_min_plus":float(min_plus)}
    return team_stat

def find_list_value(title:list[str],cur1,seas_dict,prev_dict):
    hooson=0
    tit=[]
    current=[]
    season=[]
    previous=[]
    if len(prev_dict)==0:
        hooson=1
        
    for index,value in enumerate(title):
        if title[index]==None:
            tit.append("")
            current.append("")
            season.append("")
            previous.append("")
        else:
            tit.append(value)   
            current.append(cur1[index])
            season.append(seas_dict[value])  
            temp="" if hooson else prev_dict[value]  
            previous.append(temp)
    return [tit,current,season,previous]


"""[{$match:{'t1_players.import':1}},
  {
  $unwind:"$t1_players"
},
 {$group:
  {
   "_id":"$t1_players.p_name",
    "pts":{$sum:"$t1_players.p_assist"}
  } },
  {$sort:{"pts":-1}}
  
 ]"""
# get stat and title names assign to individual dictionary keys and values
def assign_stat_to_dic(num,name,res_list):
    st={}
   
    st["plr_num"]=num
    st["plr_name"]=name
       
    for i in range(0,5):    
        st["title"+str(i)]=get_title(res_list[0][i])
        st["stat"+str(i)]=res_list[1][i]
        st["avg_stat"+str(i)]=res_list[2][i]
        st["prev_stat"+str(i)]=res_list[3][i]
            
    return(st)  
def assign_team_stat_to_dict(teams_stat,team_names):
    t_stat={}
    t_stat['name']=team_names
    t_stat['pts']=teams_stat['t_points']
    t_stat['fg']=str(teams_stat['t_fg_made'])+"/"+str(teams_stat['t_fg_attempt'])
    t_stat['fgp']=round(teams_stat['t_fg_percent'],1)
    t_stat['2p']=str(teams_stat['t_two_p_made'])+"/"+str(teams_stat['t_two_p_attempt'])
    t_stat['2pp']=round(teams_stat['t_two_p_percent'],1)
    t_stat['3p']=str(teams_stat['t_three_made'])+"/"+str(teams_stat['t_three_attempt'])
    t_stat['3pp']=round(teams_stat['t_three_p_percent'],1)
    t_stat['ft']=str(teams_stat['t_ft_made'])+"/"+str(teams_stat['t_ft_attempt'])
    t_stat['ftp']=round(teams_stat['t_ft_percent'],1)
    t_stat['o/reb']=teams_stat['t_offensive']
    t_stat['d/reb']=teams_stat['t_defensive']
    t_stat['reb']=teams_stat['t_rebound']
    t_stat['ast']=teams_stat['t_assist']
    t_stat['to']=teams_stat['t_turnover']
    t_stat['stl']=teams_stat['t_steal']
    t_stat['blck']=teams_stat['t_block']
    t_stat['foul']=teams_stat['t_foul']
    t_stat['pts_f_to']=teams_stat['pts_f_to']
    t_stat['pts_paint']=teams_stat['pts_paint']
    t_stat['sec_c_pt']=teams_stat['two_c_p']
    t_stat['pts_fast']=teams_stat['pts_fast']
    t_stat['pts_bench']=teams_stat['pts_bench']
    t_stat['lead']=teams_stat['lead']
    t_stat['score_run']=teams_stat['score_run']  
    return t_stat