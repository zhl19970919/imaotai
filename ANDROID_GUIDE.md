# 安卓手机运行指南

本指南详细介绍如何在安卓手机上使用Termux运行i茅台智能抢购工具。

## 一、准备工作

### 1. 安装Termux

#### 方法一：从F-Droid安装（推荐）
1. 在手机浏览器访问：https://f-droid.org/packages/com.termux/
2. 下载并安装Termux应用

#### 方法二：从GitHub安装
1. 访问：https://github.com/termux/termux-app/releases
2. 下载最新的APK文件
3. 在手机上安装APK

### 2. 授予Termux存储权限
首次打开Termux后，运行以下命令：
```bash
termux-setup-storage
```
选择"允许"授予存储权限。

## 二、安装Python环境

### 1. 更新包管理器
```bash
pkg update && pkg upgrade
```

### 2. 安装Python

#### 检查当前Python版本
```bash
python --version
```

如果显示Python 3.12，需要先卸载或使用pyenv安装Python 3.11。

**重要**：Termux默认安装Python 3.11+版本，这是Playwright支持的版本。Python 3.12目前不被Playwright支持。

#### 方法一：卸载并重新安装（推荐）

##### 卸载Python 3.12
```bash
pkg uninstall python
```

##### 安装Python 3.11
```bash
pkg install python
```

##### 验证Python版本
```bash
python --version
```

应该显示Python 3.11.x

#### 方法二：使用pyenv安装Python 3.11

**注意**：pyenv编译Python在Termux中可能失败，建议优先使用方法一。

如果方法一失败，可以尝试使用pyenv，但可能会遇到编译错误。

##### 安装pyenv
```bash
pkg install pyenv
```

##### 配置pyenv环境
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

##### 安装Python 3.11
```bash
pyenv install 3.11.9
```

**如果编译失败**，这是Termux环境的常见问题，建议：
1. 使用方法一（pkg install python）
2. 或者尝试安装其他版本的Python（如3.10）
3. 查看详细错误日志：`cat /data/data/com.termux/files/usr/tmp/python-build.*.log`

##### 设置Python 3.11为默认版本
```bash
pyenv global 3.11.9
```

##### 验证Python版本
```bash
python --version
```

应该显示Python 3.11.9

### 3. 验证Python安装
```bash
python --version
```
应该显示Python 3.8或更高版本。

## 三、安装项目文件

### 方法一：使用Git克隆（推荐）

1. 安装Git
```bash
pkg install git
```

2. 克隆项目（如果有Git仓库）
```bash
git clone <你的仓库地址>
cd imaotai
```

### 方法二：手动传输文件

1. 在电脑上打包项目文件
2. 通过以下方式传输到手机：
   - USB数据线传输
   - 微信/QQ文件传输
   - 云盘（百度网盘、阿里云盘等）

3. 将文件复制到Termux可访问的目录
```bash
cd ~/storage/downloads
```

4. 解压或复制文件到工作目录
```bash
mkdir -p ~/imaotai
cp -r ~/storage/downloads/imaotai/* ~/imaotai/
cd ~/imaotai
```

## 四、安装Python依赖

### 1. 升级pip
```bash
python -m pip install --upgrade pip
```

### 2. 安装Playwright

#### 方法一：使用国内镜像源（推荐）
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple playwright
```

#### 方法二：使用官方源
```bash
pip install playwright
```

如果安装失败，请尝试以下步骤：

1. 升级pip到最新版本
```bash
python -m pip install --upgrade pip
```

2. 清理pip缓存
```bash
pip cache purge
```

3. 重新安装
```bash
pip install playwright
```

### 3. 安装Chromium浏览器

**注意**：在Termux中，Playwright的Chromium可能无法正常工作。建议使用以下替代方案：

#### 方案一：使用系统浏览器（推荐）
Termux可以直接使用Android系统的浏览器，无需安装Chromium。

#### 方案二：安装Playwright浏览器（可能失败）
```bash
playwright install chromium
```

如果安装失败，可以跳过此步骤，程序会自动使用系统浏览器。

## 五、配置程序

### 1. 编辑配置文件
```bash
nano config.json
```

### 2. 填写配置信息
```json
{
  "user": {
    "phone": "你的手机号",
    "password": ""
  },
  "products": [
    {
      "name": "飞天53%vol 500ml贵州茅台酒（带杯）",
      "url": "https://h5.moutai519.com.cn/...",
      "purchase_time": "09:00:00"
    }
  ],
  "settings": {
    "headless": false,
    "timeout": 30,
    "retry_times": 3,
    "advance_seconds": 2
  }
}
```

### 3. 保存并退出
- 按 `Ctrl + O` 保存
- 按 `Enter` 确认
- 按 `Ctrl + X` 退出

## 六、获取商品URL

1. 在手机浏览器访问：https://h5.moutai519.com.cn/
2. 登录i茅台账号
3. 找到"飞天53%vol 500ml贵州茅台酒（带杯）"商品
4. 进入商品详情页
5. 复制浏览器地址栏的URL
6. 将URL填入config.json的url字段

## 七、运行程序

### 1. 运行主程序
```bash
python main.py
```

### 2. 登录流程
- 程序会自动打开浏览器窗口
- 自动点击登录按钮
- 自动输入手机号
- 自动点击获取验证码
- 收到短信后，手动编辑config.json，将验证码填入password字段
- 重新运行程序完成登录

### 3. 自动抢购
- 程序会等待到设定的抢购时间
- 自动访问商品页面
- 自动点击购买按钮
- 自动确认订单

## 八、常用命令

### 查看文件列表
```bash
ls
```

### 编辑配置文件
```bash
nano config.json
```

### 查看日志
```bash
python main.py 2>&1 | tee run.log
```

### 后台运行
```bash
nohup python main.py > run.log 2>&1 &
```

### 查看后台进程
```bash
ps aux | grep python
```

### 停止后台进程
```bash
pkill -f "python main.py"
```

## 九、常见问题

### Q1: Termux安装失败
A: 确保从官方渠道下载Termux，不要使用Google Play商店的版本（已停止维护）。

### Q2: pip安装速度慢
A: 使用国内镜像源：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple playwright
```

### Q3: pip install playwright失败，提示"No matching distribution found"
A: 这通常是Python版本或网络问题，尝试以下解决方案：

#### 解决方案1：检查Python版本
```bash
python --version
```

Playwright目前对Python 3.12的支持可能不完善。建议使用Python 3.10或3.11。

#### 解决方案2：降级Python版本（推荐）
在Termux中安装Python 3.11：
```bash
pkg install python=3.11
```

然后重新安装Playwright：
```bash
pip install playwright
```

#### 解决方案3：使用清华镜像源
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple playwright
```

#### 解决方案4：使用阿里云镜像源
```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ playwright
```

#### 解决方案5：升级pip后重试
```bash
python -m pip install --upgrade pip
pip install playwright
```

#### 解决方案6：清理缓存后重试
```bash
pip cache purge
pip install playwright
```

#### 解决方案7：查看详细错误信息
```bash
pip install playwright -v
```

如果以上方法都失败，请考虑使用Selenium替代Playwright。

### Q4: Playwright安装Chromium失败
A: 确保网络连接稳定，或使用代理：
```bash
export PLAYWRIGHT_DOWNLOAD_HOST=https://playwright.azureedge.net
playwright install chromium
```

**注意**：在Termux中，Chromium可能无法正常安装或运行。建议跳过此步骤，程序会自动使用系统浏览器。

### Q5: 浏览器启动失败
A: 在Termux中，Playwright的Chromium可能不兼容。建议：

1. 跳过`playwright install chromium`步骤
2. 程序会自动使用Android系统浏览器
3. 确保已授予Termux网络权限

### Q6: ModuleNotFoundError: No module named playwright
A: 这说明Playwright没有安装成功。由于Termux默认安装Python 3.12，而Playwright不支持Python 3.12，建议使用Selenium替代。

#### 方案一：使用Selenium替代（推荐）

Selenium对Python 3.12支持更好，是更好的选择。

##### 安装Selenium（尝试多个镜像源）

如果清华镜像源失败，可以尝试以下镜像源：

**镜像源1：阿里云（推荐）**
```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ selenium
```

**镜像源2：豆瓣镜像**
```bash
pip install -i https://pypi.douban.com/simple/ selenium
```

**镜像源3：中科大镜像**
```bash
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ selenium
```

**镜像源4：清华镜像（如果可用）**
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple selenium
```

**镜像源5：华为云镜像**
```bash
pip install -i https://mirrors.huaweicloud.com/repository/pypi/simple/ selenium
```

**镜像源6：官方源（最慢但最稳定）**
```bash
pip install selenium
```

##### 安装Chromium

**注意**：Termux中可能没有chromium包，或者安装后无法正常使用。

#### 方案A：使用Android系统浏览器（推荐）

Selenium可以直接调用Android系统浏览器，无需安装额外的浏览器。

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 配置使用Android Chrome
options = Options()
options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36')

# 使用远程WebDriver（需要Appium）
# driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
```

**注意**：这需要安装Appium，配置较复杂。

#### 方案B：使用requests库（最简单）

对于i茅台抢购工具，可以直接使用requests库发送HTTP请求，无需浏览器。

```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ requests
```

这是最简单、最稳定的方案，不需要浏览器。

#### 方案C：尝试安装chromium（可能失败）

```bash
pkg install chromium
```

如果提示包不存在，说明Termux仓库中没有chromium。

#### 方案D：使用headless浏览器

某些headless浏览器可能在Termux中可用：

```bash
# 尝试安装
pkg search chromium
pkg search firefox
pkg search webkit
```

查看可用的浏览器包。

##### 验证安装

**如果使用Selenium：**
```bash
python -c "import selenium; print(selenium.__version__)"
```

**如果使用requests：**
```bash
python -c "import requests; print(requests.__version__)"
```

如果显示版本号，说明安装成功。

##### 使用Selenium/requests运行程序

需要修改程序代码，将Playwright替换为Selenium或requests。详见下方的"方案三：使用Selenium/requests替代Playwright"。

#### 方案二：继续尝试安装Playwright

如果必须使用Playwright，可以尝试以下步骤：

##### 步骤1：检查Python版本
```bash
python --version
```

**重要**：如果显示Python 3.12，这是问题所在！

Playwright目前不支持Python 3.12，必须使用Python 3.11或更低版本。

##### 步骤2：卸载Python 3.12
```bash
pkg uninstall python
```

##### 步骤3：安装Python 3.11
```bash
pkg install python
```

**注意**：如果Termux还是安装Python 3.12，说明仓库中没有Python 3.11，请使用方案一（Selenium）。

##### 步骤4：验证Python版本
```bash
python --version
```

应该显示Python 3.11.x

##### 步骤5：清理pip缓存
```bash
pip cache purge
```

##### 步骤6：使用清华镜像源安装Playwright
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple playwright
```

##### 步骤7：验证安装
```bash
python -c "import playwright; print(playwright.__version__)"
```

如果显示版本号，说明安装成功。

##### 步骤8：如果还是失败，尝试阿里云镜像
```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ playwright
```

#### 为什么Python 3.12不兼容？
- Playwright对Python 3.12的支持还在开发中
- PyPI镜像源可能还没有同步Python 3.12兼容的Playwright版本
- Termux默认安装Python 3.12，无法通过pkg降级
- pyenv编译Python 3.11在Termux中容易失败
  - **推荐使用requests库替代**（最简单、最稳定）

### 方案三：使用Selenium/requests替代Playwright（推荐）

如果无法安装Playwright，可以使用Selenium或requests替代。

#### 方案A：使用requests库（最简单、最稳定）

对于i茅台抢购工具，可以直接使用requests库发送HTTP请求，无需浏览器。

##### 安装requests
```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ requests
```

##### 验证安装
```bash
python -c "import requests; print(requests.__version__)"
```

##### 修改程序代码

需要将程序中的Playwright代码替换为requests代码。主要区别：

1. **导入语句**
```python
# Playwright
from playwright.sync_api import sync_playwright

# requests
import requests
import json
```

2. **发送HTTP请求**
```python
# Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://h5.moutai519.com.cn/')

# requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
}
response = requests.get('https://h5.moutai519.com.cn/', headers=headers)
```

3. **处理响应**
```python
# Playwright
content = page.content()

# requests
content = response.text
data = response.json()
```

#### requests优势
- ✅ **最简单** - 无需浏览器
- ✅ **最稳定** - 不依赖浏览器驱动
- ✅ **速度快** - 直接HTTP请求
- ✅ **支持Python 3.12** - 完美兼容
- ✅ **资源占用少** - 不需要浏览器

#### requests劣势
- ❌ 无法执行JavaScript
- ❌ 需要手动处理cookies和session
- ❌ 某些复杂操作可能无法实现

#### 方案B：使用Selenium（需要浏览器）

如果必须使用浏览器，可以使用Selenium。详见上方的"方案一：使用Selenium替代"。

### Q7: 程序运行时闪退
A: 查看错误日志：
```bash
python main.py 2>&1 | tee error.log
```

常见原因：
- Python版本过低（需要3.8+）
- Playwright未正确安装
- 配置文件格式错误
- 网络连接问题
- Selenium/Playwright未正确安装
- ChromeDriver/Chromium未正确安装

### Q8: 键盘输入不方便
A: 安装Termux:API和额外键盘：
```bash
pkg install termux-api
```
然后在设置中启用Termux键盘。

### Q9: 存储空间不足
A: 清理不必要的文件：
```bash
pkg clean
```

### Q10: 如何保持Termux后台运行
A: 使用Termux:Boot或nohup命令：
```bash
nohup python main.py > run.log 2>&1 &
```

## 十、优化建议

### 1. 提高网络速度
- 使用5G或WiFi网络
- 关闭其他占用网络的应用
- 避免在网络高峰期抢购

### 2. 优化Termux性能
- 关闭不必要的后台应用
- 使用性能模式运行
- 定期清理缓存

### 3. 提前测试
- 在抢购前测试登录流程
- 测试网络速度
- 验证配置文件正确性

### 4. 监控运行状态
- 使用日志记录运行情况
- 定期检查程序状态
- 及时处理异常情况

## 十一、安全建议

1. 不要将config.json上传到公共仓库
2. 定期更换密码
3. 不要在公共网络下运行
4. 及时更新Termux和Python版本

## 十二、项目文件清单

确保以下文件都在工作目录中：
```
imaotai/
├── config.json       # 配置文件
├── main.py           # 主程序
├── login.py          # 登录模块
├── purchase.py       # 抢购模块
├── config.py         # 配置管理
├── test_browser.py   # 浏览器测试脚本
├── requirements.txt  # 依赖包
├── README.md         # 说明文档
└── ANDROID_GUIDE.md  # 安卓运行指南（本文件）
```

## 十三、快速开始

如果你已经熟悉Termux，可以快速开始：

```bash
# 1. 安装依赖
pkg update && pkg upgrade
pkg install python git

# 2. 克隆项目（如果有仓库）
git clone <仓库地址>
cd imaotai

# 3. 安装Python包
pip install playwright
playwright install chromium

# 4. 配置程序
nano config.json

# 5. 运行程序
python main.py
```

## 十四、联系支持

如果遇到问题，请：
1. 查看本文档的常见问题部分
2. 检查错误日志
3. 确认所有依赖都已正确安装
4. 验证配置文件格式正确

---

**祝您抢购成功！**
