import sqlite3,uuid,json
from be_models import registerInfo,loginInfo
from datetime import datetime


conn = sqlite3.connect("../database/data.db",check_same_thread=False)
conn.isolation_level = None
cursor = conn.cursor()

created_date = int(datetime.now().timestamp())



def create_Tables() -> dict:
  """ create tables if not found.
  Return: 
    dictionary:
  {
    status (bool)
    msg (str)
  }
  
  """

  try:
    #assistants
    cursor.execute(  """CREATE TABLE IF NOT EXISTS assistants(
      assist_id TEXT   PRIMARY KEY,
      aname CHAR(20)    NOT NULL,
      persona TEXT,
      model TEXT    NOT NULL
    )"""  )
    
  except sqlite3.Error as er:
    print(f"errorcode:{er.sqlite_errorcode}\n \
          errorname:{er.sqlite_errorname}") 
    return {
      'status' : False,
      'msg' : 'error creating assistant.'
    }  
 
 
  try: 
    #memories
    cursor.execute(  """CREATE TABLE IF NOT EXISTS memories(
      memory_id INTEGER   PRIMARY KEY AUTOINCREMENT,
      assist_id TEXT NOT NULL,
      role TEXT  NOT NULL,
      chat TEXT  NOT NULL,
      created_date INTEGER  NOT NULL,
      FOREIGN KEY (assist_id)
                      REFERENCES assistants (assist_id)
    )"""  )
    
  except sqlite3.Error as er:
    print(f"errorcode:{er.sqlite_errorcode}\n \
          errorname:{er.sqlite_errorname}") 
    return {
      'status' : False,
      'msg' : 'error creating memories.'
    }
    
   
  try:
    #users
    cursor.execute(  """CREATE TABLE IF NOT EXISTS users(
      uid TEXT   PRIMARY KEY,
      assist_id TEXT    NOT NULL,
      username TEXT   NOT NULL,
      dob INTEGER NOT NULL, 
      question INTEGER   NOT NULL,
      answer TEXT   NOT NULL,
      password BLOB   NOT NULL,
      created_date INTEGER NOT NULL,
      FOREIGN KEY (assist_id)
                      REFERENCES assistants (assist_id)
    )"""  ) 
    
  except sqlite3.Error as er:
    print(f"errorcode:{er.sqlite_errorcode}\n \
          errorname:{er.sqlite_errorname}") 
    return {
      'status' : False,
      'msg' : 'error creating users.'
    }

  return {
      'status' : True,
      'msg' : 'Successful'
    }

def create_user(regData : registerInfo) -> dict:
  
  uid : str = str(uuid.uuid1())
  assist_id : str = str(uuid.uuid3(uuid.NAMESPACE_DNS, regData.username))

  try :
    cursor.execute( " INSERT INTO assistants(assist_id,aname,persona,model) \
                  VALUES(?,?,?,?)",(assist_id,regData.aname,regData.persona,
                                    regData.model,) )

    cursor.execute( " INSERT INTO users(uid,assist_id,username,dob,question,answer,password,created_date) \
                  VALUES(?,?,?,?,?,?,?,?)",(uid,assist_id,regData.username,regData.dob,regData.qa[0],
                                    regData.qa[1],regData.password,created_date,) )

    return {
      'status' : True,
      'msg' : 'Created account successfully.'
    }

  
  except Exception as er:
    print(f"error :{er}") 
    return {
      'status' : False,
      'msg' : 'error creating users.'
    }

def check_user(username:str) -> dict:
  
  try:
    
    cursor.execute('SELECT 1 FROM users WHERE username = ?',(username,))
    result = cursor.fetchone()

    if result:
      return {
        'status' : True,
        'exist' : True,
        'msg' : 'user exist'
      }
    return {
        'status' : True,
        'exist' : False,
        'msg' : 'user not exist'
      }
    
    
  except Exception as e:
    print('Error in check_user:',e)
    return {
        'status' : False,
        'msg' : f'Exception raise: {e}'
      }
    
def get_userPass(username:str) -> dict:
  cursor.execute("SELECT password FROM users WHERE username=?",(username,))
  result = cursor.fetchone()
  if result:
    return result[0]
  
def get_userAccessData(username:str) -> dict:
  try:
    cursor.execute( "SELECT uid,assist_id FROM users WHERE username=?",
                  (username,))
    result = cursor.fetchone()  
    if result:
      return {
        'status':True,
        'data':{
        'username': username,
        'uid' : result[0],
        'assist_id' : result[1]
        }
      }
  except Exception as e:
    print("Exception in userAccessData:",e)
    return {
      'status':False,
      'msg' : 'Error accessing data.'
    }
  
def get_userAssist_data(assist_id:str) -> dict:
  
  cursor.execute(" SELECT persona,model FROM assistants WHERE assist_id = ? ",(assist_id,))
  result = cursor.fetchone()  
  
  return {
    'model' : result[1],
    'persona' : result[0]
  }
  
def save_menmory(assist_id,user:list,ai:list) -> dict:
  
  user.append(created_date)
  ai.append(created_date)
  
  fragments : list = [tuple(user),tuple(ai)]
  
  cursor.executemany( " INSERT INTO memories(assist_id,role,chat,created_date) \
                     VALUES(?,?,?,?) ", fragments)
  
  chats = get_Chats(assist_id)
  
  return chats

def get_Chats(assist_id:str) -> list:
  
  cursor.execute(" SELECT memory_id,role,chat,created_date FROM memories \
                 WHERE assist_id = ? ORDER BY memory_id DESC LIMIT 10",
                 (assist_id,))
  
  result = cursor.fetchall()
  
  chats : list[dict] = []
  
  for chat in result:
    temp = {
      'memory_id' : chat[0],
      "role" : chat[1],
      "chat" : chat[2],
      "created_date" : chat[3]
    }
    chats.append(temp)
    
  return list(reversed(chats))
  
def get_Settings(assist_id:str) -> dict:
  
  cursor.execute(" SELECT aname,model,persona FROM assistants WHERE assist_id = ?",
                  (assist_id,))
  result = cursor.fetchone()
  print("DB-result:",result)
  
  return {
    'aname' : result[0],
    'model' : result[1],
    'persona' : result[2]
  }
  
def get_userProfile(uid:str) -> dict:
  
  cursor.execute( "SELECT username,dob,created_date FROM users WHERE uid=?",
                 (uid,))
  result = cursor.fetchone()
  print("result:",result)
  return {
    'username':result[0],
    'dob' : result[1],
    'created_date' : result[2] 
  }

def update_userProfile(uid:str, **updateCols):
  print(updateCols)
  update = ''
  colName : list = [ _ for _ in updateCols if updateCols[_] ]


  for indx,x in enumerate(colName,start=1):
      update = update + f'{x} = "{updateCols[x]}"'
      if len(colName) > 1 and indx != len(colName):
          update = update + ','
      
  print("update:",update)
      
        
  try:        
    cursor.execute(f'UPDATE users SET {update} WHERE uid=?',(uid,))
    return {
      'status' : True,
      'msg': 'Updation successful.'
    }

  
  except Exception as e:
    print("error at update_userProfile:",e)
    return {
      'status' : False,
      'msg': 'Error updating users profile.'
    }
  
  
  
# if __name__ =='__main__':
  
#   data = {
#     'username': 'emkay',
#     'password' : 'Vasu@6969'
#   }
  
#   get_userData()
  
  # create_Tables()
  
  #check_user('emkay')
  # data = {"username":'emkay',
  #              "dob":1729708200,
  #              "aname":'juhi',
  #              "model":'gemma2:2b',
  #              "persona":'',
  #              "qa":[0, 'doggy'],
  #              "password":'Vasu@6969'}
  # reg = registerInfo(**data)
  # create_user(reg)

# DB.uid : c638861c-9221-11ef-8781-d0c5d3da8dc4
# DB.assist_id : 10fa9fde-db83-3fda-8fd2-3ea450795901