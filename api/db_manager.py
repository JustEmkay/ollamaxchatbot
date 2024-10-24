import sqlite3,uuid
from be_models import registerInfo
from datetime import datetime

conn = sqlite3.connect("../database/data.db",check_same_thread=False)
conn.isolation_level = None
cursor = conn.cursor()

created_date = int(datetime.now().timestamp())

usersData : dict[dict] = {
    "emkay" : {
  "uid": "33acf232-8ed2-11ef-a7b2-d0c5d3da8dc4",
  "password": "$2b$12$s8evFN28hru7KGWvjiG4Xef8FCQ1ab4v.y2M61v/To/l16bGWsRky"
}
}

tokensData = []

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
      fragment TEXT,
      FOREIGN KEY (assist_id)
                      REFERENCES assistant (assist_id)
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
    
    cursor.execute( " INSERT INTO memories(assist_id) \
                  VALUES(?)",(assist_id,) )

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


# if __name__ =='__main__':
  # create_Tables()
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