# 写死的配置信息（仅示例，实际需替换为有效值）

API_KEY = "bu2DutNRkS5yFZTjlPni6sXFVh7LHkWh"  # 替换为真实密钥
TARGET_IP = "159.138.156.179"  # 替换为目标IP地址

# 使用示例（以requests库为例）
import requests


def call_api():
    url = f"http://{TARGET_IP}/api/endpoint"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        return response.text
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None


# 调用示例
result = call_api()
print(result)
