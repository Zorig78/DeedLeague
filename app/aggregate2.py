import pymongo
import pprint
from bson.objectid import ObjectId
import time
import os
import sys
from werkzeug.utils import secure_filename
import pymongo
#from .links import import25
#from .my_functions import find_brief
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


client=pymongo.MongoClient()
mydb=client["DeedLeague"]
games_col=mydb["Games"]
plr_stats=mydb["plr_stats_fem"]
tops=mydb["top_female"]
tstemp=mydb["tstemp"]
printer=pprint.PrettyPrinter()
titles_t=['a','b',None,None,"e"]
teams_name=["БИШРЭЛТ МЕТАЛЛ","ЭРДЭНЭТ MINERS","INUT YES TLG","ХАСЫН ХҮЛЭГҮҮД","SG APES","ЗАВХАН BROTHERS","СЭЛЭНГЭ БОДОНС","DARKHAN UNITED","BCH KNIGHTS","НАЛАЙХ BISON"]
female_teams=[]
team_stat_list=['t_points','t_fg_percent','t_two_p_percent','t_three_p_percent','t_ft_percent','t_offensive','t_defensive','t_rebound','t_assist','t_turnover','t_steal','t_block','t_foul','pts_f_to','pts_paint','two_c_p','pts_fast','pts_bench']

stats_t=[15,30,45,60,65]
dic1={'a':"aa",'b':"bb",'c':"cc",'d':"dd",'e':"ee"}
dics={'a':12.3,'b':5.7,'c':6.8,'d':9.9,'e':34.6}
dic2={} #'a':"zorig",'b':"gant",'c':"uurtai",'d':"bna",'e':"shyy"
#result=find_list_value(titles_t,stats_t,"a",dic1,dic2)
#print(result)
tst=dict(sorted(dics.items(), key=lambda x: x[1],reverse=True))
print(tst)
for index,(k,v) in enumerate(tst.items()):
  if k=='c':
    print(index)
  #print(index , k, v )

def avg_stat(season,team_name,stats):
  stats=games_col.aggregate([
    {'$match':
       { 'season':{'$in':season},
          '$or':[{"t1_name":team_name},{"t2_name":team_name}]
       }
    },
    {
      '$project':
       {
         "team_name":team_name,
         "stats":
           {
                '$cond':{'if':{'$eq':["$t1_name",team_name]},'then':"$team1_stat",'else':"$team2_stat"}
           } 
       }
    },
    {'$group':
      {
          "_id":"$team_name",
          "sts": {'$avg':"$stats."+stats}
      }

    }

  ])  
  
  return stats 
#Baguudiig hargalzah stat-aar jagsaaj tuhain stat-d hargalzah bair-iig butsaana  
def stat_and_pos(t_name:str,a_stat_name):
  gg={}  
  stat_dict={}
  #baguudiin neriig hadgalsan list dotroos bagiin dundaj olon function duudna
  for team in teams_name:
    rt=avg_stat(["2025"],team,a_stat_name)
    #function-aas butssan dictionaryiin bytsiig oorchilj bagasgana {bag:stat} helbert oruulna 
    for gg in rt:
      stat_dict.update({gg['_id']:round(gg['sts'],2)})
  #baguudiin dundaj stat-iig ihees baga ruu erembelne    
  sorted_st=dict(sorted(stat_dict.items(), key=lambda x: x[1],reverse=True))
  #print(sorted_st)
  #Tuhain bagiin dundaj stat ba heddygeer bairand jagssan index-iig butsaana
  for index,(k,v) in enumerate(sorted_st.items()):
    if k==t_name:
      return [v,index+1]
    

team_avg={}  
team_str={} 
team_sts={} 
t_list=[]
team_stats=[]
for tm in teams_name: 
    team_avg['team']=tm
    for stat in team_stat_list:
        s_and_p=stat_and_pos(tm,stat)
        team_sts[stat]=s_and_p[0]
        team_sts['pos']=s_and_p[1]
        team_stats.append(team_sts)
        #print(team_stats)
        #print(tm)
        team_sts={}
    team_avg['a']=team_stats
    t_list.append(team_avg)
    team_stats=[]  # reset stat list
    team_avg={} #reset all container
    team_sts={}
    
#print(t_list)

"""team_avg['s']=t_list 
team_stats.append(team_avg)
team_avg={} 
team_avg['statistic']=t_list  
team_stats.append(team_avg)
team_avg={}"""
#print(team_stats.encode('utf8'))  

#print(team_stats)  
#print(stat_and_pos("СЭЛЭНГЭ БОДОНС","t_rebound"))
def two_team_meeting(team1,team2,limit):
  two_avg_stat=games_col.aggregate([
    {
        '$match':
          {
            '$or': [
                {
                    '$and':
                      [{'t1_name': team1 }, {'t2_name': team2}]
                }, {
                    '$and': 
                     [{'t1_name': team2 }, {'t2_name': team1}]
                }
            ]
          }
    }, 
    {
        '$sort': {'date': -1}
    }, {
        '$limit': limit
    }, 
    {
        '$addFields': {
            't1_ner': team1,
            't1_stats': {
                '$cond': 
                [
                    {'$eq': ['$t1_name', team1] }, '$team1_stat', '$team2_stat'
                ]
            }
        }
    }, 
       
    {'$group': {
      '_id': "$t1_ner",
      'avg_points': { '$avg': "$t1_stats.t_points" },
      'avg_fg_percent': { '$avg': "$t1_stats.t_fg_percent" },
      'avg_two_p_percent': { '$avg': "$t1_stats.t_two_p_percent" },
      'avg_three_p_percent': { '$avg': "$t1_stats.t_three_p_percent" },
      'avg_ft_percent': { '$avg': "$t1_stats.t_ft_percent" },
      'avg_offensive': { '$avg': "$t1_stats.t_offensive" },
      'avg_defensive': { '$avg': "$t1_stats.t_defensive" },
      'avg_rebound': { '$avg': "$t1_stats.t_rebound" },
      'avg_assist': { '$avg': "$t1_stats.t_assist" },
      'avg_turnover': { '$avg': "$t1_stats.t_turnover" },
      'avg_steal': { '$avg': "$t1_stats.t_steal" },
      'avg_block': { '$avg': "$t1_stats.t_block" },
      'avg_foul': { '$avg': "$t1_stats.t_foul" }, 
      'avg_pts_f_to': { '$avg': "$t1_stats.pts_f_to" },
      'avg_pts_paint': { '$avg': "$t1_stats.pts_paint" },
      'avg_two_c_p': { '$avg': "$t1_stats.two_c_p" },
      'avg_pts_fast': { '$avg': "$t1_stats.pts_fast" },
      'avg_pts_bench': { '$avg': "$t1_stats.pts_bench" }
      }
    } ,
    {
        '$project': {
            'date': 1, 
            't1_ner': 1, 
            'avg_points': { '$round': ["$avg_points", 1] },
            'avg_fg_percent': { '$round': ["$avg_fg_percent", 1] },
            'avg_two_p_percent': { '$round': ["$avg_two_p_percent", 1] },
            'avg_three_p_percent': { '$round': ["$avg_three_p_percent", 1] },
            'avg_ft_percent': { '$round': ["$avg_ft_percent", 1] },
            'avg_offensive': { '$round': ["$avg_offensive", 1] },
            'avg_defensive': { '$round': ["$avg_defensive", 1] },
            'avg_rebound': { '$round': ["$avg_rebound", 1] },
            'avg_assist': { '$round': ["$avg_assist", 1] },
            'avg_turnover': { '$round': ["$avg_turnover", 1] },
            'avg_steal': { '$round': ["$avg_steal", 1] },
            'avg_block': { '$round': ["$avg_block", 1] },
            'avg_foul': { '$round': ["$avg_foul", 1] },
            'avg_pts_f_to': { '$round': ["$avg_pts_f_to", 1] },
            'avg_pts_paint': { '$round': ["$avg_pts_paint", 1] },
            'avg_two_c_p': { '$round': ["$avg_two_c_p", 1] },
            'avg_pts_fast': { '$round': ["$avg_pts_fast", 1] },
            'avg_pts_bench': { '$round': ["$avg_pts_bench", 1] }
        }
    }
  ])
  return two_avg_stat  

rs=two_team_meeting("ЗАВХАН BROTHERS","ХАСЫН ХҮЛЭГҮҮД",4)
for gg in rs:
    print(gg)
