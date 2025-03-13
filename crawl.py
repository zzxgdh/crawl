import json
import os
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service  # 导入 Chrome Service 类
import time


class Crawl:
    def __init__(self):
        href_path = './suno_href'
        json_path = './suno_json'
        if not os.path.exists(href_path):
            os.makedirs(href_path)
        if not os.path.exists(json_path):
            os.makedirs(json_path)
        self.driver = self.initChromeDriver()

    def initChromeDriver(self):
        """
        初始化浏览器驱动
        """
        # 创建 Service 对象，指定驱动程序的路径
        service = Service("C:\\Users\\gdh\\Downloads\\chromedriver-win64\\chromedriver.exe")
        # 配置浏览器选项
        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=C:\\Users\\gdh\\AppData\\Local\\Google\\Chrome\\User Data")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 隐藏自动化特征
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 禁用自动化提示
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument('--start-maximized')
        chrome_options.page_load_strategy = 'eager'  # 页面加载策略
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def getHomeCategory(self, email: str | None, password: str | None, category):
        """
        使用自动化工具登录主页，并且点击种类分栏
        """
        # 打开Suno登录页
        self.driver.get("https://suno.com/")
        time.sleep(5)
        # 创建ActionChains对象,后续需要点击进入suno的category目录
        home = self.driver.find_element(By.CSS_SELECTOR, "#discover-feed-container")
        # 滚动主页面滚轮
        self.driver.execute_script("""
                    const element = arguments[0];
                    const target = element.scrollHeight;
                    const duration = 22000; // 滚动时间（毫秒）
                    const start = element.scrollTop;
                    const startTime = performance.now();
    
                    function scroll() {
                        const now = performance.now();
                        const time = Math.min(1, (now - startTime) / duration);
                        element.scrollTop = start + 30000*time;
                        if (time < 1) requestAnimationFrame(scroll);
                    }
                    requestAnimationFrame(scroll);
                """, home)
        time.sleep(22)
        home_context = self.driver.find_element(By.XPATH,
                                                f'//*[@id="discover-feed-container"]/div/div/div[@aria-label="section-{category}"]/div/div[1]/a/div')
        home_context.click()
        time.sleep(5)
        # driver.execute_script("Object.defineProperties(navigator,{webdriver:{get:()=>false}});")
        # time.sleep(2)
        #
        # #点击登录按钮
        # login_button = driver.find_element(By.XPATH,'//*[@id="main-container"]/div[1]/div/div[2]/div[1]/div/div[2]/button[1]')
        # login_button.click()
        # time.sleep(2)
        # #进入账号登录
        # micro_login = driver.find_element(By.XPATH,'//*[@id=":r2:"]/div[1]/div/div/div/div[1]/div[2]/div[1]/div/button[4]')
        # micro_login.click()
        # time.sleep(5)
        # #填写账号
        # micro_email_input = driver.find_element(By.CSS_SELECTOR,'#i0116')
        # micro_email_input.send_keys(email)
        # time.sleep(2)
        # micro_email_input_confirm = driver.find_element(By.CSS_SELECTOR,'#idSIButton9')
        # micro_email_input_confirm.click()
        # time.sleep(5)
        # #填写密码
        # micro_password = driver.find_element(By.CSS_SELECTOR,'#i0118')
        # micro_password.send_keys(password)
        # driver.execute_script("Object.defineProperties(navigator,{webdriver:{get:()=>false}});")
        # time.sleep(2)
        # micro_password_confirm = driver.find_element(By.CSS_SELECTOR,'#idSIButton9')
        # micro_password_confirm.click()
        # time.sleep(4)
        # try:
        #     login_confirm = driver.find_element(By.CSS_SELECTOR,'#acceptButton')
        #     login_confirm.click()
        #     time.sleep(10)
        # except Exception as e:
        #     print(e)
        # finally:
        #     # human_verify = driver.find_element(By.CSS_SELECTOR,'#uATa8 > div > label > input[type=checkbox]')
        #     # human_verify.click()
        #     time.sleep(5)

    def getCategoryPageInfo(self, category):
        """
        获取风格种类页面的所有数据
        """
        # # 打开Suno的分栏页面
        url_suffex = quote(category)
        self.driver.get("https://suno.com/style/" + url_suffex)
        time.sleep(6)
        category_context = self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div[1]/div[3]/div/div')
        # 滚动style页面滚轮
        self.driver.execute_script("""
                    const element = arguments[0];
                    const start = element.scrollTop;
                    const startTime = performance.now();
                    
                    // 用户输入参数
                    const speedPerSecond = 500; // 每秒滚动500px
                    const duration = 60000;      // 总持续时间
                    
                    // 计算理论总滚动距离（可能超出实际可滚动范围）
                    const totalDistance = speedPerSecond * (duration / 1000);
                    
                    function scroll() {
                        const now = performance.now();
                        const elapsed = now - startTime; // 已过去的时间（毫秒）
                        const timeRatio = Math.min(elapsed / duration, 1); // 时间进度比例 0~1
                        
                        // 直接按时间比例计算滚动位置（不检查是否超出实际可滚动范围）
                        const newScrollTop = start + totalDistance * timeRatio;
                        element.scrollTop = newScrollTop;
                    
                        // 未超时则继续滚动（即使实际无法滚动也会继续执行）
                        if (elapsed < duration) {
                            requestAnimationFrame(scroll);
                        }
                    }
                    
                    requestAnimationFrame(scroll);
                """, category_context)
        time.sleep(60)
        song_father = self.driver.find_element(By.XPATH,
                                               '/html/body/div/div/div[2]/div[2]/div/div[1]/div[1]/div[3]/div/div/div')
        songs = song_father.find_elements(By.XPATH, './div')
        songs_href = []
        for song_element in songs:
            songs_href.append(
                song_element.find_element(By.XPATH, './div/div/div/div/div[2]/div[1]/div[1]/span/a').get_attribute(
                    "href"))
        with open(f'./{category}_href.txt', encoding='utf-8', mode='w') as f:
            for i in songs_href:
                f.write(i + "\n")
        print("链接保存至" + f"./{category}_href.txt")
        # songs_info = []
        # for index,element_href in enumerate(songs_href):
        #     songs_info.append(self.getSongInfoByHref(driver,element_href,index+1))
        # with open(f"./{category}_songs.json",encoding="utf-8",mode='w') as f:
        #     json.dump(songs_info,f,indent=4)
        # print("信息保存至"+f"./{category}_songs.json")
        time.sleep(1)

    def getSongInfoByHref(self, href, index):
        """
        根据id获取内容并返回字典
        """
        dict = {}
        dict['href'] = href
        # self.driver.execute_script(f"window.open('{dict['href']}');")
        # # 切换到新标签页
        # handles = self.driver.window_handles
        # self.driver.switch_to.window(handles[-1])
        self.driver.execute_script(f"window.location.href='{href}'")  # 从打开新标签页转为替换本地页面

        time.sleep(3)
        # 显式等待页面加载
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-container"]'))
        )
        # 提取数据
        dict['title'] = self.driver.find_element(By.XPATH,
                                                 '//*[@id="main-container"]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/a').text
        dict['prompt'] = self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div/div/div/div/a[1]').text
        dict['version'] = self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div/div/div/div/span[2]').text
        dict['lyrics'] = self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div/div/div/div/section').text
        # #关闭新标签页
        # self.driver.close()
        # # 切换回原标签页
        # self.driver.switch_to.window(handles[0])
        time.sleep(1)
        print('成功爬取第' + str(index) + '条歌曲: ' + dict['title'] + ' 链接: ' + dict['href'])
        return dict

    def getAllUsers(self):
        """
        获取用户列表
        """
        col = int(input("选择爬取用户第几列(1-4):"))
        if col>4 or col<1:
            return
        self.driver.get("https://suno.com/search?type=user")
        time.sleep(4)
        self.driver.find_element(By.XPATH,
                                 '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div/div[3]').click()
        time.sleep(4)

        userScroll = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div[2]')
        # 滚动页面滚轮,设置时间s秒
        scrollTime = 60
        self.driver.execute_script("""
                            const element = arguments[0];
                            const start = element.scrollTop;
                            const startTime = performance.now();

                            // 用户输入参数
                            const speedPerSecond = 500; // 每秒滚动500px
                            const duration = arguments[1]*1000;      // 总持续时间

                            // 计算理论总滚动距离（可能超出实际可滚动范围）
                            const totalDistance = speedPerSecond * (duration / 1000);

                            function scroll() {
                                const now = performance.now();
                                const elapsed = now - startTime; // 已过去的时间（毫秒）
                                const timeRatio = Math.min(elapsed / duration, 1); // 时间进度比例 0~1

                                // 直接按时间比例计算滚动位置（不检查是否超出实际可滚动范围）
                                const newScrollTop = start + totalDistance * timeRatio;
                                element.scrollTop = newScrollTop;

                                // 未超时则继续滚动（即使实际无法滚动也会继续执行）
                                if (elapsed < duration) {
                                    requestAnimationFrame(scroll);
                                }
                            }

                            requestAnimationFrame(scroll);
                        """, userScroll, scrollTime)
        time.sleep(scrollTime + 1)
        '//*[@id="react-aria-:R9kvepl87ltplfb:-tabpanel-user"]/div/div[2]/div[1]'

        # 等待父元素加载
        usersElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="react-aria-:R9kvepl87ltplfb:-tabpanel-user"]/div/div[2]/div')))
        users = []
        for user in usersElement:
            try:
                userInfo = user.find_element(By.XPATH, './div[1]/span[1]').text
                users.append(userInfo)
            except Exception as e:
                print("部分元素显示不充分")
        with open("./users.txt", encoding="utf-8", mode="w") as f:
            for index, userId in enumerate(users):
                if (index + 1) % 4 == col:
                    f.write(userId + "\n")
        print("用户id保存至" + "users.txt")

    def getSongIdFromUsers(self):
        """
        根据users.txt的用户与已经下载的suno_href里面的txt进行对比，获取现在需要下载的用户群体
        """
        users = []
        with open("./users.txt", encoding="utf-8", mode="r") as f:
            for line in f:
                users.append(line.strip())
        #获取保存的歌手列表
        suno_href = [f for f in os.listdir('./suno_href') if os.path.exists('./suno_href')]
        print("从第"+str(len(suno_href))+"个用户开始爬取数据!")
        for index,userId in enumerate(users):
            if index >= (len(suno_href)-1):
                self.getSongIdByUserId(userId,index)
        print("爬取完毕!")

    def getSongIdByUserId(self,userId,index):
        """
        根据用户的ID获取其创作的歌曲id
        """
        self.driver.get("https://suno.com/"+userId)
        time.sleep(5)
        userScroll = self.driver.find_element(By.XPATH,'//*[@id="main-container"]/div[1]')
        # 滚动页面滚轮,设置时间s秒
        scrollTime = 180
        self.driver.execute_script("""
                                    function smoothScrollWithPause(element, totalTimeSec) {
                                        const totalTimeMs = totalTimeSec * 1000;
                                        let currentPosition = element.scrollTop;
                                        let elapsedTime = 0;
                                        let accumulatedDistance = 0;
                                        // 每段参数配置
                                        const segmentConfig = {
                                            scrollSpeed: 500,       // 每秒滚动500px
                                            segmentDistance: 1500,  // 每段滚动距离
                                            pauseDuration: 1000,    // 段间停顿时间
                                            get scrollDuration() {  // 每段滚动时间（3秒）
                                                return (this.segmentDistance / this.scrollSpeed) * 1000;
                                            }
                                        };
                                    
                                        // 关键动画函数
                                        function animateScroll(targetPosition, duration) {
                                            return new Promise(resolve => {
                                                const startTime = performance.now();
                                                
                                                function step(currentTime) {
                                                    const progress = Math.min((currentTime - startTime) / duration, 1);
                                                    element.scrollTop = currentPosition + (targetPosition - currentPosition) * progress;
                                                    
                                                    if (progress < 1) {
                                                        requestAnimationFrame(step);
                                                    } else {
                                                        resolve();
                                                    }
                                                }
                                                requestAnimationFrame(step);
                                            });
                                        }
                                    
                                        // 主控制逻辑
                                        (async function execute() {
                                            while (elapsedTime < totalTimeMs) {
                                                // 计算本段可用时间
                                                const remainingTime = totalTimeMs - elapsedTime;
                                                const shouldPause = accumulatedDistance >= segmentConfig.segmentDistance;
                                                
                                                // 执行段间停顿
                                                if (shouldPause && remainingTime > segmentConfig.pauseDuration) {
                                                    await new Promise(r => setTimeout(r, segmentConfig.pauseDuration));
                                                    elapsedTime += segmentConfig.pauseDuration;
                                                    accumulatedDistance = 0;  // 重置累计距离
                                                    continue;
                                                }
                                    
                                                // 计算本段滚动距离和时间
                                                const scrollTime = Math.min(
                                                    remainingTime,
                                                    segmentConfig.scrollDuration
                                                );
                                                const scrollDistance = (scrollTime / 1000) * segmentConfig.scrollSpeed;
                                                
                                                // 执行平滑滚动
                                                await animateScroll(currentPosition + scrollDistance, scrollTime);
                                                
                                                // 更新状态
                                                currentPosition += scrollDistance;
                                                accumulatedDistance += scrollDistance;
                                                elapsedTime += scrollTime;
                                            }
                                        })();
                                    }
                                    smoothScrollWithPause(arguments[0], arguments[1]);
                                """, userScroll, scrollTime)
        time.sleep(scrollTime + 1)
        songs_element = self.driver.find_elements(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div[2]/div')
        song_hrefs = []
        for song_element in songs_element:
            try:
                song_href = song_element.find_element(By.XPATH, './div[2]/div[1]/a').get_attribute("href")
                song_hrefs.append(song_href)
            except Exception as e:
                pass
        with open(f"./suno_href/{userId}.txt",encoding='utf-8',mode='w') as f:
            for href in song_hrefs:
                f.write(href+"\n")
        print("第"+str(index+1)+"个用户获取信息完毕!")


if __name__ == "__main__":
    crawl = Crawl()
    # 先根据1-4列获取对应的用户
    # crawl.getAllUsers()
    # 再通过用户获取对应的歌曲id保存至suno_href
    crawl.getSongIdFromUsers()
    # 最后通过id得到歌曲内容
