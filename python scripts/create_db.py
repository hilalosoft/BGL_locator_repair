import sqlite3

def create_db():
    # filename to form database
    file = "BGLocators.db"
    try:
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        query = "CREATE TABLE locator (id integer,textcase varchar,dir_path varchar,e_class varchar,e_name varchar,e_value varchar,e_type varchar,e_alt varchar,src varchar,href varchar,size varchar,onclick varchar,height varchar,width varchar,xpath varchar,xaxis varchar,yaxis varchar,img_b64 varchar);"
        cursor.execute(query)
        print("Database BGLocators.db was created the table locator was created.")
    except:
        print("Database BGLocators.db not created.")

def main():
    create_db()

if __name__=="__main__":
    main()