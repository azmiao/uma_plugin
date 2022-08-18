import os
import json
import base64

# 生成图片结果
async def get_img_cq(img_path):
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'properties.json'), 'r') as f:
        config = json.load(f)
    if config['image_send_form']['current'] == 'file':
        return f'[CQ:image,file=file:///{os.path.abspath(img_path)}]'
    else:
        with open(img_path, 'rb') as imgf:
            img_base = str(base64.b64encode(imgf.read()), encoding='utf-8')
        return f'[CQ:image,file=base64://{img_base}]'