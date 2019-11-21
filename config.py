# Redis数据库地址
REDIS_HOST = "localhost"

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = ""

# Redis名称
REDIS_NAME = "gushiwen"


# 古诗文登陆地址
LOGIN_URL = "https://so.gushiwen.org/user/login.aspx?from="

# 古诗文登陆后的地址
LOGINED_URL = "https://so.gushiwen.org/user/collect.aspx"


# 验证码保存路径
CAPTCHA_PATH = './captcha.png'

# 验证码名称
CAPTCHA_NAME = 'captcha.png'

# 产生器默认使用的浏览器
DEFAULT_BROWSER = 'Chrome'

# API地址和端口
API_HOST = '127.0.0.1'
API_PORT = 5000

# 产生器和验证器循环周期
CYCLE = 120

# 进程开关
# 产生器，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = True