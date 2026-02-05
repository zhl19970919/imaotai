import requests
from config import Config
import time
from datetime import datetime
import re
from bs4 import BeautifulSoup


class Purchase:
    def __init__(self, config: Config, session):
        self.config = config
        self.session = session
        self.settings = config.get_settings()

    def wait_for_purchase_time(self, purchase_time):
        while True:
            now = datetime.now()
            target_time = datetime.strptime(purchase_time, '%H:%M:%S').replace(
                year=now.year,
                month=now.month,
                day=now.day
            )
            
            advance_seconds = self.settings.get('advance_seconds', 2)
            wait_time = (target_time - now).total_seconds() - advance_seconds
            
            if wait_time <= 0:
                print(f"抢购时间到！当前时间: {now.strftime('%H:%M:%S')}")
                break
            
            if wait_time > 60:
                print(f"等待抢购时间: {purchase_time}，还需等待 {int(wait_time // 60)} 分钟")
                time.sleep(60)
            else:
                print(f"即将开始抢购，还需等待 {int(wait_time)} 秒")
                time.sleep(1)

    def purchase_product(self, product):
        product_url = product.get('url', '')
        product_name = product.get('name', '')
        quantity = product.get('quantity', 1)
        
        if not product_url:
            print(f"商品 {product_name} 未配置URL，跳过")
            return False
        
        print(f"开始抢购商品: {product_name}")
        print(f"购买数量: {quantity} 瓶")
        print(f"访问商品页面: {product_url}")
        
        try:
            response = self.session.get(product_url)
            print(f"访问商品页面成功，状态码: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print("查找商品ID...")
            product_id = self._extract_product_id(soup, product_url)
            
            if product_id:
                print(f"商品ID: {product_id}")
                return self._submit_order(product_id, quantity, product_name)
            else:
                print("未找到商品ID，尝试直接提交订单")
                return self._submit_order_direct(product_url, quantity, product_name)
                
        except Exception as e:
            print(f"抢购过程出错: {e}")
            return False

    def _extract_product_id(self, soup, url):
        try:
            product_id = None
            
            method1 = soup.find('input', {'name': 'productId'})
            if method1:
                product_id = method1.get('value')
            
            if not product_id:
                method2 = soup.find('div', {'class': re.compile(r'product.*id', re.I)})
                if method2:
                    product_id = method2.get('data-product-id')
            
            if not product_id:
                match = re.search(r'/product/(\d+)', url)
                if match:
                    product_id = match.group(1)
            
            return product_id
        except Exception as e:
            print(f"提取商品ID失败: {e}")
            return None

    def _submit_order(self, product_id, quantity, product_name):
        print(f"提交订单: 商品ID={product_id}, 数量={quantity}")
        
        try:
            order_api_url = "https://h5.moutai519.com.cn/gw/api/order/add"
            order_data = {
                "productId": product_id,
                "quantity": quantity,
                "deliveryType": 1
            }
            
            response = self.session.post(order_api_url, json=order_data)
            print(f"订单提交响应: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"订单结果: {result}")
                
                if result.get('code') == 2000:
                    print(f"✓ 商品 {product_name} 抢购成功！购买数量: {quantity} 瓶")
                    return True
                else:
                    print(f"✗ 商品 {product_name} 抢购失败: {result.get('msg', '未知错误')}")
                    return False
            else:
                print(f"订单提交失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"提交订单出错: {e}")
            return False

    def _submit_order_direct(self, product_url, quantity, product_name):
        print(f"尝试直接提交订单: {product_url}")
        
        try:
            order_api_url = "https://h5.moutai519.com.cn/gw/api/order/add"
            order_data = {
                "productUrl": product_url,
                "quantity": quantity,
                "deliveryType": 1
            }
            
            response = self.session.post(order_api_url, json=order_data)
            print(f"订单提交响应: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"订单结果: {result}")
                
                if result.get('code') == 2000:
                    print(f"✓ 商品 {product_name} 抢购成功！购买数量: {quantity} 瓶")
                    return True
                else:
                    print(f"✗ 商品 {product_name} 抢购失败: {result.get('msg', '未知错误')}")
                    return False
            else:
                print(f"订单提交失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"提交订单出错: {e}")
            return False

    def run_purchase(self):
        products = self.config.get_products()
        
        for product in products:
            purchase_time = product.get('purchase_time', '09:00:00')
            print(f"等待抢购时间: {purchase_time}")
            
            self.wait_for_purchase_time(purchase_time)
            
            retry_times = self.settings.get('retry_times', 3)
            for i in range(retry_times):
                print(f"第 {i + 1} 次尝试抢购")
                success = self.purchase_product(product)
                if success:
                    print("抢购成功，程序结束")
                    break
                time.sleep(0.5)
