 # Crawl

## 配置
运行前确保谷歌浏览器已经登录过suno
>
    谷歌浏览器的驱动器在https://googlechromelabs.github.io/chrome-for-testing/#stable里面找对应版本下载
    chrome_options.add_argument("--user-data-dir=C:\\Users\\gdh\\AppData\\Local\\Google\\Chrome\\User Data")
    将此处的浏览器用户配置修改为自己本地的
  
 ### 使用selenium模拟用户浏览器进行访问，可以获取用户信息和通过用户信息获取歌曲id信息，最后爬取歌曲。

 >
    # 先根据1-4列获取对应的用户
    crawl.getAllUsers()
    # 再通过用户获取对应的歌曲id保存至suno_href
    crawl.getSongIdFromUsers()
    # 最后通过id得到歌曲内容

## 运行
```
pip install selenium
python crawl.py
