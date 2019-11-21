from db import AccountRedisClient

'''
输入账号密码并保存到redis数据库中
'''

def set(account, password):
    conn = AccountRedisClient()
    result = conn.set(account, password)
    print('账号', account, '密码', password)
    print('录入成功' if result else '录入失败')



def AccountInput():
    while True:
     account = input("请输入账号：(输入exit退出)")
     if account == 'exit':
         break
     else:
        password = input("请输入密码：")
        set(account, password)


if __name__ == "__main__":
    AccountInput()

