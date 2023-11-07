import subprocess


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
    
    def connect():
    
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )    
        cur = conn.cursor()
        return conn, cur

def replace_conf_cmd(configuration, task, conf_type, key):
    
    param = task[conf_type][key]
    param = db_host.replace("{","") 
    param = db_host.replace("}","") 
    param = task["configuration"][param]

    return param

def parse_shell(task, configuration):
    
    command = task["content"]["command"]
    out_content = subprocess.check_output(command, shell=True)
    if "outputFile" in task["content"]:
        output_f = task["content"]["outputFile"]
        
        with open(output_f,'wb') as fw:
            fw.write(out_content)
        return b''
    return out_content

def parse_database(task, configuration):

    db_host = replace_conf_cmd(configuration, task, "connection", "dbHost")
    db_user = replace_conf_cmd(configuration, task, "connection", "dbUser")
    db_pwd = replace_conf_cmd(configuration, task, "connection", "dbPwd")
    db_name = replace_conf_cmd(configuration, task, "connection", "dbName")


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
        for row in rows:
            print(row)


def parse_task(task, configuration):
    if task["type"]=="shell":
        result = parse_shell(task, configuration)        
        return result.decode('utf-8')
    
    elif task["type"]=="database":
        result = parse_database(task, configuration)        
    else:
        print("Type not found")
    return ""