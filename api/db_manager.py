import sqlite3

conn = sqlite3.connect("../database/data.db",check_same_thread=False)
conn.isolation_level = None
cursor = conn.cursor()



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
    #memories
    cursor.execute(  """CREATE TABLE IF NOT EXISTS memories(
      memory_id INTEGER   PRIMARY KEY AUTOINCREMENT,
      fragment TEXT   NOT NULL
    )"""  )
    
  except sqlite3.Error as er:
    print(f"errorcode:{er.sqlite_errorcode}\n \
          errorname:{er.sqlite_errorname}") 
    return {
      'status' : False,
      'msg' : 'error creating memories.'
    }
    

  try:
    #assistants
    cursor.execute(  """CREATE TABLE IF NOT EXISTS assistants(
      assist_id INTEGER   PRIMARY KEY AUTOINCREMENT,
      aname CHAR(20)    NOT NULL,
      persona TEXT NOT NULL,
      model TEXT    NOT NULL,
      memory_id INTEGER   NOT_NULL,
      FOREIGN KEY (memory_id)
                      REFERENCES memories (memory_id)
    )"""  )
    
  except sqlite3.Error as er:
    print(f"errorcode:{er.sqlite_errorcode}\n \
          errorname:{er.sqlite_errorname}") 
    return {
      'status' : False,
      'msg' : 'error creating assistant.'
    }  
  
  try:
    #users
    cursor.execute(  """CREATE TABLE IF NOT EXISTS users(
      uid INTEGER   PRIMARY KEY AUTOINCREMENT,
      assist_id INTEGER    NOT NULL,
      username TEXT   NOT NULL,
      dob INTEGER NOT NULL, 
      qa TEXT   NOT NULL,
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



# if __name__ =='__main__':
#   create_Tables()