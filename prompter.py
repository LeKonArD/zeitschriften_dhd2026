from tqdm import tqdm
import pandas as pd
import requests
import json
import os
import re

def prompt(coreprompt, model):
    response = requests.post(
                                      url="https://openrouter.ai/api/v1/chat/completions",
                                      headers={
                                        "Authorization": "Bearer "+openrouter_key,
                                      },
                                      data=json.dumps({
                                        "model": model, # Optional
                                        "messages": [
                                          {
                                            "role": "user",
                                            "content": coreprompt
                                          }
                                        ]
                                      })
                                    )
    return response


parser = argparse.ArgumentParser(description='Sends prompt and text data to openrouter and stores answers')
parser.add_argument('--inputpath', type=str, help='openrouter-api-key')
parser.add_argument('--key', type=str, help='openrouter-api-key')
parser.add_argument('--model', type=str, help='model bezeichnung in openrouter')
parser.add_argument('--prompt', type=str, help='Basis Prompt')
parser.add_argument('--outfile', type=str, help='Pfad zum Speichern der Antworten')
args = parser.parse_args()

inputpath = args.inputpath
openrouter_key = args.key
prompt = args.prompt
outfile = args.outfile
model = args.model

output = []
files = os.listdir(inputpath)

for fname in tqdm(files):
    try:
        
        myprompt = prompt+open(fname,"r").read()
        
        res = prompt(myprompt, model)
        res = json.loads(res.content)["choices"][0]["message"]["content"]
        res = re.sub("^.*\{","{",res, flags=re.DOTALL)
        res = re.sub("}.*","}",res, flags=re.DOTALL)
        res = json.loads(res)
    
        res["fname"] = fname
        output.append(res)
        
        result = pd.DataFrame(output)
        result.to_csv(outfile, sep="\t")
        
    except:
        pass
