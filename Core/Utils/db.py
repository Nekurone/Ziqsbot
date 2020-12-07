import json

def load_json(file: str) -> dict:
    '''
    Very basic wrapper for loading jsons into dicts
    strict is False to ensure control characters allowed
    '''
    if not file.endswith('.json'):
        file = file + '.json'
    f = json.load(open(file,'r'),strict=False)

def dump_json(file:str,
              data:dict):
    '''
    Very basic wrapper for saving dicts to json file
    '''
    if not file.endswith('.json'):
        file = file + '.json'
    with open(file, 'w') as f:
        json.dump(f, data)
    
