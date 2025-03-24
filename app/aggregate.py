import pymongo
import pprint
from bson.objectid import ObjectId
from .links import import25
from .my_functions import find_brief

client=pymongo.MongoClient()
mydb=client["DeedLeague"]
games_col=mydb["Games"]
plr_stats=mydb["plr_stats_fem"]
tops=mydb["top_female"]
tstemp=mydb["tstemp"]
printer=pprint.PrettyPrinter()
#Багийг авсан хожлоор нь жагсааж харуулна
def teamStands(season,male):
  standing=[]
  s1={}
  s2={}
  stand=games_col.aggregate(
  [ 
    {"$match":{ "$and":
              [     
                    {"male":male},
                    {"season":season}
                    
              ]  
              }
    },
    {
      "$group":{"_id":"$t1_name",
      "wins":{"$sum":"$t1_win"}}
    }
    
    ])
  stand2=games_col.aggregate(
  [ 
    {"$match":{ "$and":
              [     
                    {"male":male},
                    {"season":season}
                    
              ]  
              }
    },
    {
      "$group":{"_id":"$t2_name",
      "wins":{"$sum":"$t2_win"}}
    }
    
  ])
  # Python Dict Update
  # marks = {'Physics':67, 'Maths':87}
  # internal_marks = {'Practical':48}
  # marks.update(internal_marks)
  # Output: {'Physics': 67, 'Maths': 87, 'Practical': 48}
  
  # home bagaar togloson yalaltiig s1-d hadgalna 
  for yy in stand:
    s1.update({yy["_id"]:yy["wins"]})
  # zochin bagaar togloson yalaltiig s2-d hadgalna   
  for zz in stand2:
    s2.update({zz["_id"]:zz["wins"]})  
  
  # Nogoo dict dotorhi key buyu bagiin ner davhtsaj baival yalaltiig nemne baihgyi bol utgiig onoono
  for k,v in s2.items():
      if k in s1:
        s1[k]+=v
      else:
        s1[k]=v
  #standing.append(s1)  
  #standing.append(s2)
  #print(s1)
  return s1

stand1=teamStands("2024",1)    
#printer.pprint(list(stand1)) 


def stat1(seas):
  return games_col.aggregate(
  [ 
    {"$match":{ "$and":
              [     
                    {"male":0},
                    {"season":seas}
                    
              ]  
              }
    },
    
    {"$unwind":"$t1_players"},
    {"$match":
              {
                "t1_players.p_status":{"$gt":0},
                "t1_players.import" : 0
              }
    }, 
  
    {"$group":
      {"_id":"$t1_players.p_name",
      "teams":{"$last":"$t1_players.team"},
      "t_pts":{"$sum":"$t1_players.p_points"},
      "fgm":{"$sum":"$t1_players.fg_made"},
      "fga":{"$sum":"$t1_players.fg_attempt"},
      "fgp":{"$avg":"$t1_players.p_fg_percent"},
      "two_pt_m":{"$sum":"$t1_players.two_p_made"},
      "two_pt_a":{"$sum":"$t1_players.two_p_attempt"},
      "two_pt_per":{"$avg":"$t1_players.p_two_p_percent"},
      "three_pt_m":{"$sum":"$t1_players.three_p_made"},
      "three_pt_a":{"$sum":"$t1_players.three_p_attempt"},
      "three_pt_per":{"$avg":"$t1_players.p_three_p_percent"},
      "ft_m":{"$sum":"$t1_players.ft_made"},
      "ft_a":{"$sum":"$t1_players.ft_attempt"},
      "ft_per":{"$avg":"$t1_players.p_ft_percent"},
      "off_reb":{"$sum":"$t1_players.p_offensive"},
      "def_reb":{"$sum":"$t1_players.p_defensive"},
      "tot_reb":{"$sum":"$t1_players.p_rebound"},
      "assist":{"$sum":"$t1_players.p_assist"},
      "to":{"$sum":"$t1_players.p_turnover"},
      "steal":{"$sum":"$t1_players.p_steal"},
      "block":{"$sum":"$t1_players.p_block"},
      "blocked":{"$sum":"$t1_players.p_blocker"},
      "p_foul":{"$sum":"$t1_players.p_p_foul"},
      "foul_on":{"$sum":"$t1_players.p_fouls_on"},
      "min_plus":{"$sum":"$t1_players.p_min_plus"},
      "played":{"$sum":"$t1_players.p_status"},
      "win":{"$sum":"$t1_players.win"},
      "starter":{"$sum":"$t1_players.starter"},
      "tot_sec":{"$sum":"$t1_players.p_totals"}          
      }
    },
    {"$sort":{"ppg":-1}}
  ])  
#print(players_stats)



def removeFields(fieldName):
  games_col.update_many({},{"$unset":{fieldName:1}})    
#removeFields("t1.players.import")




def additionalField():
  names=[]
  cursor=games_col.find({})
  for x in cursor:
    rel_id=x["_id"]
    t1_name=x["t1_name"]
    t1_pts=x["t1_score"]
    t2_name=x["t2_name"]
    t2_pts=x["t2_score"]
    if int(t1_pts)>int(t2_pts):
      t1_win=1
    else:
      t1_win=0
    dbResponse=games_col.update_one({"_id":ObjectId(rel_id)},{"$set":{"t1_win":t1_win}})

    #print(t1_name,t1_pts,t2_name,t2_pts,t1_win,names)

def addWin():
  ## add winning flag to each player 
  names=[]
  cursor=games_col.find({})
  for x in cursor:
    rel_id=x["_id"]
    t1_name=x["t1_name"]
    t2_name=x["t2_name"] 
    t1_win=x["t1_win"]
    t2_win=x ["t2_win"]
    t1_player_names=x["t1_players"]
    for pname in t1_player_names:
      team_name=pname["team"]

      played_g=pname["p_status"]
      #print(f"{t1_name}=={team_name}--->{played_g}")
      
      if(played_g!=0):
        if (team_name==t1_name):
          games_col.update_one({"_id":ObjectId(rel_id)},{"$set":{"t1_players.$[element].win":t1_win}},array_filters=[{"element.team":t1_name}])
        else:
          games_col.update_one({"_id":ObjectId(rel_id)},{"$set":{"t1_players.$[element].win":t2_win}},array_filters=[{"element.team":t2_name}])

      """if(played_g==0):
        games_col.update_one({"_id":ObjectId(rel_id)},{"$set":{"t1_players.$[element].win":0}},array_filters=[{"element.team":t1_name}])  """

      #### remove nested doc field
      ###games_col.update_one({"_id":ObjectId(rel_id)},{"$unset":{"t1_players.$[].win":1}})
#addWin()


def topFifty(coef1,coef2,coef3):
  cont={}
  plrs=plr_stats.find({})
  for every in plrs:
    # positive stats 
    names=every["_id"]
    teams=every['teams']
    tpts=every['t_pts']
    fgm=every['fgm']
    fga=every['fga']
    fg_p=every['fgp']
    two_pm=every['two_pt_m']
    two_pa=every['two_pt_a']
    two_pp=every['two_pt_per']
    three_pm=every['three_pt_m']
    three_pa=every['three_pt_a']
    three_pp=every['three_pt_per']
    ft_m=every['ft_m']
    ft_a=every['ft_a']
    ft_per=every['ft_per']
    tot_reb=every['tot_reb']
    assist=every['assist']
    block=every['block']
    steal=every['steal']
    fls_on=every['foul_on']
    min_plus=every['min_plus']
    #negative stats 
    to=every['to']
    fls=every['p_foul']
    blocked=every['blocked']

    wins=every['win']
    starters=every['starter']
    played=every['played']

    pos_pts=tpts+fgm+fga+fg_p+two_pa+ two_pm+ two_pp+three_pa+ three_pm+ three_pp+ ft_a+ ft_m+ ft_per+ tot_reb+coef3*(assist+block+steal)+fls_on+min_plus
    neg_pts=to+fls+blocked
    if(wins>played):
      wins=played
    if played>0:
      win_p=(wins/played)
      if starters==0:
        starters=0.05
        starter_p=starters/played
      else:
        starter_p=starters/played
    else:
      win_p=0  
      starter_p=0
    win_p=coef1*win_p
    starter_p=coef2*starter_p
    pts=(pos_pts-neg_pts)*win_p*starter_p
    if played>5:
        cont={
              "name":names,
              "team":teams,
              "pos_pts":pos_pts,
              "neg_pts":neg_pts,
              "win_p":win_p,
              "strt_p":starter_p,
              "played":played,
              "scores":pts     
        }
        tops.insert_one(cont)
    else:
      continue    
###------ add team2 win 
def addSecondField():
  cursor2=games_col.find({})
  for line in cursor2:
    rel_id=line["_id"]
    t1_win=line["t1_win"]  
    t2_win=1-t1_win
    games_col.update_one({"_id":ObjectId(rel_id)},{"$set":{"t2_win":t2_win}})
#addSecondField()

tshoot=[]
def getTShooting():
  true_shoot={}
  cursor3=plr_stats.find({})
  for xx in cursor3:
    names1=xx["_id"]
    teams1=xx['teams']
    tpts1=xx['t_pts']
    fga1=xx['fga']
    fta1=xx['ft_a']
    played1=xx['played']
    if(fta1!=0) and (fga1!=0):
      ts=tpts1/(2*(fga1+(0.44*fta1))) 
    else:
      ts=0
    if played1>5:
      true_shoot={
        "_id":names1,
        "team":teams1,
        "ts":ts
      }
      tstemp.insert_one(true_shoot)
  """  tshoot.append(true_shoot)
  tshoot1=sorted(tshoot,key=lambda k:k['ts'])  
  print(tshoot1)  
  return tshoot1"""
   

#getTShooting()
    

###  ---sorting leaders from temp collection
def getTops():
  num=0
  tables=tops.find({},{"_id":0,"name":1,"team":1,"played":1,"scores":1},sort=[('scores',pymongo.DESCENDING)]).limit(30)
  for rows in tables:
    num=num+1
    names=rows['name']
    teams=rows['team']
    scores=rows['scores']
    played=rows['played']
    
    
    if teams in stand1:
      num_win=stand1[teams]
      num_lose=10-num_win
    scr=round(scores,3)
    #print(f"{played} ")
    print(f"({num_win}-{num_lose}) ")

#printer.pprint(list(tables)) 

def indivStat():
  list_per=[]
  all=[]
  ind_stat=plr_stats.find({},{"_id":1,"teams":1,"t_pts":1,"played":1},sort=[('t_pts',pymongo.DESCENDING)]).limit(20)
  for rows1 in ind_stat:
    played=rows1['played']
    if played>5:
      names=rows1['_id']
      teams=rows1['teams']
      scores=rows1['t_pts']
      apg=scores/played
      scr=round(apg,2)
      dict_per={
        "name":names,
        "team":teams,
        "per_stat":scr,
        "played":played
      }
      list_per.append(dict_per)
      #print(f"{scores} ")
  all=sorted(list_per,key=lambda x: x["per_stat"],reverse=True )  
  for record in all:
    ners=record['name']
    bag=record['team']
    stat_per=record['per_stat']
    played_num=record['played']
    print(f"{played_num}")
#indivStat()

""" ------MOST STAT BY EACH GAME------ """
def mostStats(male,season,frgn,bracket):
  most=games_col.aggregate(
    [
      {
          '$match': {
              'male': male, 
              'season': season
          }
      }, {
          '$unwind': '$t1_players'
      }, {
          '$match': {
              't1_players.import': frgn
          }
      }, {
          '$sort': {
              't1_players.three_p_made': -1
          }
      }, {
          '$limit': bracket
      }
    ])
  return most

def listMost():
  cursor4=mostStats(1,"2024",0,10)
  for row3 in cursor4:
    ner=row3.get("t1_players")
    #name=ner['p_block']
    #team=row3['t1_players.team']
    most_pts=ner['p_name']
    three_made=ner['three_p_made']
    print(f" {most_pts}------{three_made}")
    
#listMost()

def teamPtsAvg(male,season):
  standing=[]
  s1={}
  s11={}
  s2={}
  s22={}
  home_team=games_col.aggregate(
  [ 
    {"$match":{ "$and":
              [     
                    {"male":male},
                    {"season":season}
                    
              ]  
              }
    },
    {
      "$group":{"_id":"$t1_name",
      "pts_taken":{"$avg":"$t1_score"},
      "pts_given":{"$avg":"$t2_score"}}
    }
    
    ])
  away_team=games_col.aggregate(
  [ 
    {"$match":{ "$and":
              [     
                    {"male":male},
                    {"season":season}
              ]  
              }
    },
    {
      "$group":{"_id":"$t2_name",
      "pts_taken":{"$avg":"$t2_score"},
      "pts_given":{"$avg":"$t1_score"}}
    }
    
  ])
  for yy in home_team:
    s1.update({yy["_id"]:yy["pts_taken"]})
    s11.update({yy["_id"]:yy["pts_given"]})
  for zz in away_team:
    s2.update({zz["_id"]:zz["pts_taken"]})  
    s22.update({zz["_id"]:zz["pts_given"]}) 
  ##pts taken  
  for k,v in s2.items():
      if k in s1:
        s1[k]=(s1[k]+v)/2
      else:
        s1[k]=v
  ##pts given        
  for k,v in s22.items():
      if k in s11:
        s11[k]=(s11[k]+v)/2
      else:
        s11[k]=v      
  mostPts=dict(sorted(s1.items(),key=lambda item:item[1],reverse=True))
  lostPts=dict(sorted(s11.items(),key=lambda item:item[1]))  
  ### --------------------Tsaashdaa emhleh shaardlagatai 
  print(mostPts)
  print(lostPts)
  return s1  

#teamPtsAvg(1,"2024")

""" ------FUNCTIONS CALL------ """
#topFifty(1,1,1)
#getTops()
#addWin()
#additionalField()
#add fields in array
#x=games_col.update_many({"t1_name":"ХОВД ЧАНДМАНЬ"},{"$set":{"t1_name":"AC SCORPIONS"}})
#print(x.modified_count, "documents updated.")

"""----top player list-------"""
"""players_stats=stat1("2024")
for single in players_stats:
  plr_stats.insert_one(single)
printer.pprint(list(players_stats)) """



#---->update array elements
#res=games_col.update_many({},{"$set":{"t1_players.$[element].win":0}},array_filters=[{"element.p_status":0}])
#res=games_col.update_many({},{"$set":{"t1_players.$[element].team":"AC SCORPIONS"}},array_filters=[{"element.team":"KHOVD"}])
#printer.pprint(list(res))




def teamStats(male,season,field,types):
  s1={}
  s2={}
  t1_stat="$team1_stat."+field
  t2_stat="$team2_stat."+field
  home_team=games_col.aggregate(
  [ 
    {"$match":{ "$and":
              [     
                    {"male":male},
                    {"season":{
                        '$in': season
                      }
                    }
                    
              ]  
              }
    },
    {
      "$group":{"_id":"$t1_name",
      "t1_field":{types:t1_stat},
      }
    }
    
    ])
  away_team=games_col.aggregate(
  [ 
    {"$match":{ "$and":
              [     
                    {"male":male},
                    {"season":{
                        '$in': season
                      }
                    }
              ]  
              }
    },
    {
      "$group":{"_id":"$t2_name",
      "t2_field":{types:t2_stat},}
    }
    
  ])
  for yy in home_team:
    s1.update({yy["_id"]:yy["t1_field"]})
   
  for zz in away_team:
    s2.update({zz["_id"]:zz["t2_field"]})  
  ##pts taken  
  for k,v in s2.items():
      if k in s1:
        if types=="$avg":
            s1[k]=(s1[k]+v)/2
        else: 
            s1[k]=(s1[k]+v)   
      else:
        s1[k]=v
      
  out_stat=dict(sorted(s1.items(),key=lambda item:item[1],reverse=True))
   
  ### --------------------Tsaashdaa emhleh shaardlagatai 
  #print(out_stat)
 
  return out_stat

# Bagiin stat-iig songoson talbart ulirlaar ni torloor ni(sum,avg) haruulna 
def getStats():
  season=["2023","post2023"]
  list1=teamStats(1,season,"t_assist","$avg")
  key_val=list1.keys()
  for each_key in key_val:
    print(each_key)
  val=list1.values()
  for each_val in val:
    print(round(each_val,2))
#getStats()    


'''
2 ba tyynees deesh utga haihdaa
[
    {
        '$match': {
            '$and': [
                {
                    'season':   
                      {
                        '$in': ['2023', 'post2023']
                      }
                }, 
                  {'male': 1 }
            ]
        }
    }
]

-------------------------------------------Player Individual Stat-------------------------------------
[
    {
        '$match': {
            'male': 1, 
            'season': {
                '$in': [
                    '2024', 'post2024'
                ]
            }
        }
    }, {
        '$unwind': '$t1_players'
    }, {
        '$match': {
            't1_players.p_name': 'Munkh-Erdene Shinebileg'
        }
    }, {
        '$group': {
            '_id': '$t1_players.p_name', 
            't_pts': {
                '$sum': '$t1_players.p_points'
            }, 
            't_played': {
                '$sum': '$t1_players.p_status'
            }
        }
    }, {
        '$set': {
            'av_pts': {
                '$divide': [
                    '$t_pts', '$t_played'
                ]
            }
        }
    }
]
'''

def change_team_name(old_val,new_val):
    query_filter={'t1_name' : old_val} #{"t2_name":old_val}
    update_operation ={"$set":{"t1_name":new_val}} # 
    
    result = games_col.update_many(query_filter, update_operation)
    return result
#change_team_name("KHULEGUUD","ХАСЫН ХҮЛЭГҮҮД")
#change("ХАСЫН ХҮЛЭГҮҮД","ОМНИ ХҮЛЭГҮҮД")

def change(old_val,new_val):
    query_filter={'t1_players.team' : old_val} #{"t2_name":old_val}
    update_operation ={ '$set' : { 't1_players.$[element].team' : new_val}} # {"$set":{"t2_name":new_val}}
    
    result = games_col.update_many(query_filter, update_operation,array_filters=[{"element.team":old_val}])
    return result

#change("KHULEGUUD","ХАСЫН ХҮЛЭГҮҮД")


#Ner tom jijgeer bichigdsen bol zasna
'''cursor=games_col.find({})
for x in cursor:
  t1_player_names=x["t1_players"]
  for pname in t1_player_names:
      player_name=pname["p_name"]
      change_name=player_name.title()
      change(player_name,change_name)'''

      
## array elementiin utga oorchiloh, talbar nemehed ashiglana
def change_import(plr):
    query_filter={'t1_players.p_name' : plr} #'t1_players.p_name' : Ishtaya Jambal
    update_operation ={ '$set' : { 't1_players.$.import' : 0}}
    result = games_col.update_many(query_filter,{'$set':{'t1_players.$.import':1}} ) #,array_filters=[{ "elem.import": { "$exists": False } }] # filter ashiglah bol $-araas [elem] nemj ogno
    return result
#list dotor baigaa toglogchdiin import solino
#for plr in import25:
#  change_import(plr)  



#Батцэцэг Батбаатар,Batsetseg Batbaatar,Болор-Эрдэнэ Баатар,Bolor-Erdene Baatar,Болор-эрдэнэ Амараа,Bolor-Erdene Amaraa",
# Булган Баярхүү,Bulgan Bayarkhuu,Дэлгэрцэцэг Мягмарсүрэн,Delgertsetseg Myagmarsuren, Иштаяа Жамбал ,Ishtaya Jambal,
# Маамуу Пүрэв,Maamuu Purev,Намуундарь Намхайнямбуу,Namuundari Namkhainyambuu, Уянга Алтансүх ,Uyanga Altansukh ,
# Халиун Төмөрхуяг ,Хонгорзул Алтанзул,Khongorzul Altanzul

def avg_plr_stat(plr_name,season):
  plr_avg={}
  stats_avg=games_col.aggregate(
  [
    {
        '$match': {
            'male': 1, 
            'season': {
                '$in': season
            }, 
            't1_players.p_name': plr_name
        }
    }, {
        '$unwind': '$t1_players'
    }, {
        '$match': {
            't1_players.p_name': plr_name
        }
    }, {
        '$group': {
            '_id': '$t1_players.p_name', 
            "t_pts":{"$sum":"$t1_players.p_points"},
            "fgm":{"$sum":"$t1_players.fg_made"},
            "fga":{"$sum":"$t1_players.fg_attempt"},
            "fgp":{"$sum":"$t1_players.p_fg_percent"},
            "two_pt_m":{"$sum":"$t1_players.two_p_made"},
            "two_pt_a":{"$sum":"$t1_players.two_p_attempt"},
            "two_pt_per":{"$sum":"$t1_players.p_two_p_percent"},
            "three_pt_m":{"$sum":"$t1_players.three_p_made"},
            "three_pt_a":{"$sum":"$t1_players.three_p_attempt"},
            "three_pt_per":{"$sum":"$t1_players.p_three_p_percent"},
            "ft_m":{"$sum":"$t1_players.ft_made"},
            "ft_a":{"$sum":"$t1_players.ft_attempt"},
            "ft_per":{"$sum":"$t1_players.p_ft_percent"},
            "off_reb":{"$sum":"$t1_players.p_offensive"},
            "def_reb":{"$sum":"$t1_players.p_defensive"},
            "tot_reb":{"$sum":"$t1_players.p_rebound"},
            "assist":{"$sum":"$t1_players.p_assist"},
            "to":{"$sum":"$t1_players.p_turnover"},
            "steal":{"$sum":"$t1_players.p_steal"},
            "block":{"$sum":"$t1_players.p_block"},
            "blocked":{"$sum":"$t1_players.p_blocker"},
            "p_foul":{"$sum":"$t1_players.p_p_foul"},
            "foul_on":{"$sum":"$t1_players.p_fouls_on"},
            "min_plus":{"$sum":"$t1_players.p_min_plus"},
            "played":{"$sum":"$t1_players.p_status"},
            "win":{"$sum":"$t1_players.win"},
            "starter":{"$sum":"$t1_players.starter"},
            "tot_sec":{"$sum":"$t1_players.p_totals"}          
            
            
        }
    },
    {"$project": { 
                    "pts" :{"$divide":["$t_pts","$played"]},
                    "fgm" :{"$divide":["$fgm","$played"]},
                    "fga" :{"$divide":["$fga","$played"]},
                    "fgp" :{"$divide":["$fgp","$played"]},
                    "2pm" :{"$divide":["$two_pt_m","$played"]},
                    "2pa" :{"$divide":["$two_pt_a","$played"]},
                    "2pp" :{"$divide":["$two_pt_per","$played"]},
                    "3pa" :{"$divide":["$three_pt_a","$played"]},
                    "3pm" :{"$divide":["$three_pt_m","$played"]},
                    "3pp" :{"$divide":["$three_pt_per","$played"]},
                    "fta" :{"$divide":["$ft_a","$played"]},
                    "ftm" :{"$divide":["$ft_m","$played"]},
                    "ftp" :{"$divide":["$ft_per","$played"]},
                    "oreb":{"$divide":["$off_reb","$played"]},
                    "dreb":{"$divide":["$def_reb","$played"]},
                    "reb": {"$divide":["$tot_reb","$played"]},
                    "ass" :{"$divide":["$assist","$played"]},
                    "to":{"$divide":["$to","$played"]},
                    "stl":{"$divide":["$steal","$played"]},
                    "blk":{"$divide":["$block","$played"]},
                    "min_pl":{"$divide":["$min_plus","$played"]}

            }
   
    }	
  ])

  have_list=True if stats_avg.alive else False
  if have_list==True:
    for season_avg in stats_avg:
      plr_avg['pts']=round(season_avg['pts'],1)
      plr_avg['fg']=str(round(season_avg['fgm'],1))+"/"+str(round(season_avg['fga'],1))
      plr_avg['fgp']=round(season_avg['fgp'],1)
      plr_avg['2p']=str(round(season_avg['2pm'],1))+"/"+str(round(season_avg['2pa'],1))
      plr_avg['2pp']=round(season_avg['2pp'],1)
      plr_avg['3p']=str(round(season_avg['3pm'],1))+"/"+str(round(season_avg['3pa'],1))
      plr_avg['3pp']=round(season_avg['3pp'],1)
      plr_avg['ft']=str(round(season_avg['ftm'],1))+"/"+str(round(season_avg['fta'],1))
      plr_avg['ftp']=round(season_avg['ftp'],1)
      plr_avg['reb']=round(season_avg['reb'],1)
      plr_avg['ast']=round(season_avg['ass'],1)
      plr_avg['to']=round(season_avg['to'],1)
      plr_avg['stl']=round(season_avg['stl'],1)
      plr_avg['blck']=round(season_avg['blk'],1)
      plr_avg['pl_min']=round(season_avg['min_pl'],1)
  else: plr_avg={}  
  
  return plr_avg 

#Bagiin syyliin togloltiin yr dyn  
def last_games(team_name,limit):
  game_res=[]
  gms=games_col.aggregate([
    {
        '$match': {
            '$or': [ {'t1_name': team_name }, {'t2_name': team_name } ]
        }
    }, {
        '$sort': {
            'date': -1
        }
    }, {
        '$limit': limit
    }, {
        '$project': {
            "_id":0,
            't1_name': 1, 
            't2_name': 1, 
            't1_score': 1, 
            't2_score': 1, 
            'date': 1
        }
    }])
  for gm in gms:
    if gm['t2_name']==team_name:
      temp_name=gm['t2_name']
      temp_score=gm['t2_score']
      gm['t2_name']=gm['t1_name']
      gm['t2_score']=gm['t1_score']
      gm['t1_name']=temp_name
      gm['t1_score']=temp_score
    gm['t1_short']=find_brief(gm['t1_name'])
    gm['t2_short']=find_brief(gm['t2_name'])
    game_res.append(gm)
  print(game_res)  
  return game_res  

def find_team_avg_stat(season,team_name,stat_name):
  avg_stats=games_col.aggregate([
    {
      '$match': 
        {
            'season': {'$in':season }, 
            '$or': [{'t1_name': team_name }, {'t2_name': team_name } ]
        }
    }, {
        '$project': {
            'team_name': team_name, 
            'stats': {
                '$cond': {
                    'if': {
                        '$eq': [
                            '$t1_name', team_name
                        ]
                    }, 
                    'then': '$team1_stat', 
                    'else': '$team2_stat'
                }
            }
        }
    }, {
        '$group': {
            '_id': '$team_name', 
            'avgStats': {
                '$avg': '$stats.'+stat_name
            }
        }
    }
    ])
  return list(avg_stats)

teams25_male=["БИШРЭЛТ МЕТАЛЛ","ЭРДЭНЭТ MINERS","INUT YES TLG","ХАСЫН ХҮЛЭГҮҮД","SG APES","ЗАВХАН BROTHERS","СЭЛЭНГЭ БОДОНС","BCH KNIGHTS","DARKHAN UNITED","НАЛАЙХ BISON"]
team_stat=["t_points","t_fg_percent","t_two_p_percent","t_three_p_percent","t_ft_percent","t_offensive","t_defensive","t_rebound","t_assist","t_turnover",
           "t_steal","t_block","t_foul","pts_f_to","pts_paint","two_c_p","pts_fast","pts_bench"]
for tm in teams25_male:
  ff=find_team_avg_stat(["2025"],tm,"t_rebound")  
  for ee in ff:
    print(ee['_id'].encode('utf-8') )
    print(ee['avgStats'])
  

