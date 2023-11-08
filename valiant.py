import fire
import json
from parser.cmd_parser import parse_task

def run(script_file, verbose=False):

    with open(script_file) as fs_read:
        content = fs_read.read()
    script_content  = json.loads(content)
    
    
    for task in script_content["tasks"]:
        if verbose:
            print("Running {}".format(task["id"]))
        print(parse_task(task))


fire.Fire({
    'run': run
    
})