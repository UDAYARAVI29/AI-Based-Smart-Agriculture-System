import sys, pathlib, json
sys.path.insert(0, r'C:\Users\udayaravi\Downloads\smart_agri_project\smart_agri_project\backend')
from fastapi.testclient import TestClient
import src.main as main
from pathlib import Path

client = TestClient(main.app)

# 1) Disease image upload
# Use the absolute temp_uploads folder you provided for disease test images
img_dir = Path(r'C:\Users\udayaravi\Downloads\smart_agri_project\temp_uploads')
res1 = None
if img_dir.exists():
    # find any image file in nested class folders
    found = None
    for sub in img_dir.glob('**/*'):
        if sub.is_file() and sub.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            found = sub
            break
    if found:
        with open(found, 'rb') as f:
            files = {'file': (found.name, f, 'image/jpeg')}
            res1 = client.post('/predict/disease/', files=files)
    else:
        def _dummy_json(*a, **k):
            return {'error': 'no image files found in processed disease test folder'}
        res1 = type('R', (), {'status_code': None, 'json': staticmethod(_dummy_json)})()
else:
    def _dummy_json(*a, **k):
        return {'error': f'missing test folder {img_dir}'}
    res1 = type('R', (), {'status_code': None, 'json': staticmethod(_dummy_json)})()

# 2) Yield prediction
payload_yield = {'crop':'rice','area':1.0,'rainfall':100,'temperature':30,'season':'kharif','soil_type':'loam','ph':6.5,'fertilizer_level':2}
res2 = client.post('/predict/yield/', json=payload_yield)

# 3) Fertilizer endpoint
res3 = client.post('/predict/fertilizer/')

print('DISEASE:', res1.status_code, res1.json())
print('YIELD:', res2.status_code, res2.json())
print('FERTILIZER:', res3.status_code, res3.json())
