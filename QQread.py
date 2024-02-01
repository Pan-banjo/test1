"""
获取QQ阅读的《穷爸爸富爸爸》的文本
"""
import requests
from bs4 import BeautifulSoup
import requests

session = requests.Session()

# 模拟登录
login_url = 'https://example.com/login'
login_data = {
    'username': '',
    'password': 'your_password'
}
session.post(login_url, data=login_data)

url = 'https://book.qq.com/book-read/23601930/12'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
article_content = soup.find(id='article').get_text()


print(article_content)
# 指定保存文件的路径和文件名
file_path = './QQread/QoorRich.txt'

# 打开文件并写入文本内容
with open(file_path, 'a', encoding='utf-8') as file:
    file.write(article_content)

print(f'文本内容已保存到文件: {file_path}')

