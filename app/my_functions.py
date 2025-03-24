from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select;
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import csv
from selenium.webdriver.support.color import Color
from selenium.common.exceptions import NoSuchElementException
import pymongo
import pprint
from .links import import25
global plr_stat,common_team_name,title_name
def title_name(titler):
    if titler in ["pts"]:
        title_name="ОНОО"
    elif titler in ["fg"]:
        title_name="ДОВ"   
    elif titler in ["fgp"]:
        title_name="ДОВ% "  
    elif titler in ["2p"]:
        title_name="2Pt"   
    elif titler in ["2pp"]:
        title_name="2Pt%"    
    elif titler in ["3p"]:
        title_name="3pt"   
    elif titler in ["3pp"]:
        title_name="3pt%"    
    elif titler in ["ft"]:
        title_name="Ч/шид"   
    elif titler in ["ftp"]:
        title_name="Ч/шид%"   
    elif titler in ["reb"]:
        title_name="Сам"   
    elif titler in ["ast"]:
        title_name="Дам"  
    elif titler in ["to"]:
        title_name="Б/алд"   
    elif titler in ["stl"]:
        title_name="Тас" 
    elif titler in ["blck"]:
        title_name="Хаалт"   
    elif titler in ["pl_min"]:
        title_name="+/-"
    elif titler=="":
        title_name=""
 
    return title_name                         

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
        blocker=sel_row.find_element(By.XPATH,".//td[22]/span").text
        p_foul=sel_row.find_element(By.XPATH,".//td[23]/span").text
        fouls_on=sel_row.find_element(By.XPATH,".//td[24]/span").text
        min_plus=sel_row.find_element(By.XPATH,".//td[25]/span").text

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
    blocker=sel_row.find_element(By.XPATH,".//td[22]/span").text
    p_foul=sel_row.find_element(By.XPATH,".//td[23]/span").text
    fouls_on=sel_row.find_element(By.XPATH,".//td[24]/span").text
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
