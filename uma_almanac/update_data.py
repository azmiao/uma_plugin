import os
import json

# 创建文件
async def create_json(_current_dir):
    if not os.path.exists(_current_dir):
        data = {}
        with open(_current_dir, "w", encoding="UTF-8") as f:
            json.dump(data, f)
        return data
    else:
        with open(_current_dir, 'r', encoding = 'UTF-8') as f:
            config = json.load(f)
        return config

# 写入信息
async def write_info(*args):
    group_id = args[0]
    user_id = args[1]
    _current_dir = os.path.join(os.path.dirname(__file__), f'data/{group_id}.json')
    config = await create_json(_current_dir)
    config[user_id] = {
        "actions": args[2],
        "characters": args[3],
        "fortune": args[4],
        "position": args[5],
        "prefertime": args[6],
        "suitable": [
            args[7],
            args[8]
        ],
        "unsuitable": [
            args[9],
            args[10]
        ]
    }
    with open(_current_dir, "w", encoding="UTF-8") as f:
        f.write(json.dumps(config, ensure_ascii=False, indent=4))