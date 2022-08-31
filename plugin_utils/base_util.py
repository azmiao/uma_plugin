import os
import json
import base64

from hoshino import logger

prop_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'properties.json')

# 生成图片结果
async def get_img_cq(img_path):
    with open(prop_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    if config['image_send_form']['current'] == 'file':
        return f'[CQ:image,file=file:///{os.path.abspath(img_path)}]'
    else:
        with open(img_path, 'rb') as imgf:
            img_base = str(base64.b64encode(imgf.read()), encoding='utf-8')
        return f'[CQ:image,file=base64://{img_base}]'

# 获取当前默认服务器
async def get_server_default():
    with open(prop_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    if config['default_server']['current'] not in ['jp', 'tw', 'ko', 'bili']:
        logger.critical(f'马娘插件默认服务器填写错误：{config["default_server"]["current"]}，现已将其恢复默认值jp')
        config['default_server']['current'] = 'jp'
        with open(prop_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    return config['default_server']['current']

# 获取当前设定的资源更新时间间隔 | 不使用异步
def get_interval():
    with open(prop_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    if config['res_update_cycle']['current'] not in [1, 2, 3, 4, 5, 6, 7]:
        logger.critical(f'马娘插件资源自动更新的时间间隔填写错误：{config["res_update_cycle"]["current"]}，现已将其恢复默认值1')
        config['res_update_cycle']['current'] = 1
        with open(prop_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    return config['res_update_cycle']['current']

# 获取当前代理 | 不使用异步
def get_proxy() -> dict:
    with open(prop_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    proxy_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'proxy.json')
    with open(proxy_path, 'r', encoding='utf-8') as f:
        proxy_config = json.load(f)
    if config['if_use_proxy']['current']:
        return proxy_config
    else:
        return {}

# 获取当前自动更新类型
async def get_update_type():
    with open(prop_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    if config['code_auto_update']['current'] not in ['auto', 'no']:
        logger.critical(f'马娘插件代码自动更新类型填写错误：{config["code_auto_update"]["current"]}，现已将其恢复默认值auto')
        config['code_auto_update']['current'] = 'auto'
        with open(prop_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    return config['code_auto_update']['current']