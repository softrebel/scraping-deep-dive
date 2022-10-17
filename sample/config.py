import os
import json 

os.chdir(os.path.dirname(__file__))


def write_json(output,filename):
    with open(f'{filename}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(output,ensure_ascii=False,indent=4))