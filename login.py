import requests
from config import Config
import time
import json


class Login:
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.moutaichina.com/',
            'Origin': 'https://www.moutaichina.com'
        })

    def start_session(self):
        print("正在访问i茅台官网...")
        try:
            response = self.session.get('https://www.moutaichina.com/')
            print(f"访问成功，状态码: {response.status_code}")
            return True
        except Exception as e:
            print(f"访问失败: {e}")
            return False

    def login(self):
        phone = self.config.get_phone()
        password = self.config.get_password()
        
        if not phone:
            raise ValueError("请先在config.json中配置手机号")

        print("正在访问i茅台官网...")
        try:
            response = self.session.get('https://www.moutaichina.com/')
            print(f"访问成功，状态码: {response.status_code}")
        except Exception as e:
            print(f"访问失败: {e}")
            return False
        
        time.sleep(2)
        
        print("尝试获取登录接口信息...")
        
        try:
            login_api_url = "https://www.moutaichina.com/gw/api/user/login/sendSmsCode"
            login_data = {
                "phone": phone
            }
            
            print(f"发送验证码到: {phone}")
            response = self.session.post(login_api_url, json=login_data)
            print(f"验证码发送响应: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"响应内容: {result}")
                
                print(f"请输入收到的验证码（当前密码字段: {password}）")
                print("提示：如果需要手动输入验证码，请在config.json中更新password字段")
                
                if password:
                    print("使用验证码登录...")
                    verify_api_url = "https://www.moutaichina.com/gw/api/user/login/verifySmsCode"
                    verify_data = {
                        "phone": phone,
                        "code": password
                    }
                    
                    response = self.session.post(verify_api_url, json=verify_data)
                    print(f"登录响应: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"登录结果: {result}")
                        
                        if result.get('code') == 2000:
                            print("登录成功！")
                            return True
                        else:
                            print(f"登录失败: {result.get('msg', '未知错误')}")
                            return False
                    else:
                        print(f"登录请求失败: {response.status_code}")
                        return False
                else:
                    print("未提供验证码，请在config.json中配置password字段")
                    return False
            else:
                print(f"验证码发送失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"登录过程出错: {e}")
            return False

    def close(self):
        self.session.close()
        print("会话已关闭")
