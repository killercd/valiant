import subprocess
import psycopg2
import csv

class ShellException(Exception):
    "Shell command failed"
    pass


class DatabaseParser():
    
    def __init__(self, 
                    host,
                    database,
                    user,
                    password,
                    port=5432):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
    
    def connect(self):
    
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )    
        cur = conn.cursor()
        return conn, cur

def parse_shell(task):
    
    command = task["content"]["command"]
    out_content = subprocess.check_output(command, shell=True)
    if "outputFile" in task["content"]:
        output_f = task["content"]["outputFile"]
        
        with open(output_f,'wb') as fw:
            fw.write(out_content)
        return b''
    return out_content

def parse_database(task):

    db_host = task["connection"]["host"]
    db_user = task["connection"]["user"]
    db_pwd = task["connection"]["password"]
    db_name = task["connection"]["dbname"]


    db_parser = DatabaseParser(db_host,
                                db_name,
                                db_user,
                                db_pwd)
    
    conn, cur = db_parser.connect()
    op_type = task["content"]["type"]
    if op_type=="SELECT":
        query = task["content"]["command"]
        cur.execute(query)
        rows = cur.fetchall()
        if not "output" in task["content"]:
            for row in rows:
                print(row)
        else:
            outputs = task["content"]["output"]["formats"]
            for out_format in outputs:
                if out_format["type"]=="csv":
                    with open(out_format["file"], 'w', encoding='UTF8') as f:
                        writer = csv.writer(f, delimiter =out_format["delimiter"])
                        for row in rows:
                            writer.writerow(row)



def parse_task(task):
    if task["type"]=="shell":
        result = parse_shell(task)
        return result.decode('utf-8')
    
    elif task["type"]=="database":
        result = parse_database(task)
    else:
        print("Type not found")
    return ""