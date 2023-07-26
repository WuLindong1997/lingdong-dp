import json

def load_json(input_path,encoding='utf-8'):
    with open(input_path,'r',encoding=encoding) as f:
        data=[]
        while True:
            line=f.readline()
            if not line:
                return data
            data.append(json.loads(line))

def load_json_yield(input_path,encoding='utf-8',segment_size=1024):
    with open(input_path,'r',encoding=encoding) as f:
        data = []
        while True:
            line=f.readline()
            if not line:
                return data
            data.append(json.loads(line))
            if len(data) == segment_size:
                yield data
                data = []
    
def save_json(res,output_path,mode='w',encoding='utf-8'):
    with open(output_path,mode=mode,encoding=encoding,) as f:
        for i in range(len(res)):       
            json.dump(res[i],f,ensure_ascii=False)
            f.write('\n')