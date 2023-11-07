import fire
import json
from parser.cmd_parser import parse_task

def run(script_file):

    with open(script_file) as fs_read:
        content = fs_read.read()
    script_content  = json.loads(content)
    
    configuration = script_content["configuration"]
    for task in script_content["tasks"]:
        print(parse_task(task, configuration))


fire.Fire({
    'run': run
    
})